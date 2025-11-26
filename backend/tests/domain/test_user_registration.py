"""Userドメインエンティティのテスト"""

import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError
from typing import Union, Dict

from app.domain.user import User
from app.domain.user_repository import UserRepository
from app.domain.registration_service import RegistrationService


def test_create_user_with_valid_attributes():
    """有効な属性でUserエンティティを作成できる"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password_here"
    )

    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password_here"
    assert user.id is not None  # UUIDが自動生成される
    assert user.is_active is True  # デフォルト値
    assert user.created_at is not None  # 自動設定される


def test_create_user_with_invalid_email_raises_error():
    """無効なメールアドレスでUserを作成するとエラーになる"""
    with pytest.raises(ValidationError):
        User(
            email="invalid-email",
            hashed_password="hashed_password_here"
        )


def test_create_user_with_empty_password_raises_error():
    """空のパスワードでUserを作成するとエラーになる"""
    with pytest.raises(ValidationError):
        User(
            email="test@example.com",
            hashed_password=""
        )


def test_create_user_with_empty_email_raises_error():
    """空のメールアドレスでUserを作成するとエラーになる"""
    with pytest.raises(ValidationError):
        User(
            email="",
            hashed_password="hashed_password_here"
        )


def test_cannot_instantiate_abstract_user_repository():
    """抽象クラスUserRepositoryは直接インスタンス化できない"""
    from app.domain.user_repository import UserRepository
    
    with pytest.raises(TypeError):
        UserRepository()


def test_user_repository_interface_has_find_by_email_method():
    """UserRepositoryインターフェースにfind_by_emailメソッドが定義されている"""
    from app.domain.user_repository import UserRepository

    assert hasattr(UserRepository, 'find_by_email')


def test_user_repository_interface_has_find_by_id_method():
    """UserRepositoryインターフェースにfind_by_idメソッドが定義されている"""
    from app.domain.user_repository import UserRepository

    assert hasattr(UserRepository, 'find_by_id')


# プロパティベースドテスト  
@given(st.emails())
def test_user_with_any_valid_email_is_created(email):
    """有効なメールアドレスならUserを作成できる（プロパティベースド）"""
    user = User(email=email, hashed_password="valid_password")
    # Userが正常に作成され、メールアドレスが設定されている
    assert user.email is not None
    assert "@" in user.email

@given(st.text(min_size=1))
def test_user_with_any_non_empty_password_is_created(password):
    """空でないパスワードならUserを作成できる（プロパティベースド）"""
    user = User(email="test@example.com", hashed_password=password)
    assert user.hashed_password == password


@given(st.emails(), st.text(min_size=1))
def test_user_always_has_valid_uuid(email, password):
    """生成されたUserは常に有効なUUIDを持つ（プロパティベースド）"""
    user = User(email=email, hashed_password=password)
    assert user.id is not None
    assert user.id.version == 4  # UUID v4


# RegistrationService テスト

class InMemoryUserRepository(UserRepository):
    """テスト用のインメモリUserRepository実装"""

    def __init__(self):
        self._users: Dict[str, User] = {}

    def save(self, user: User) -> User:
        self._users[user.email] = user
        return user

    def find_by_email(self, email: str) -> Union[User, None]:
        return self._users.get(email)

    def find_by_id(self, user_id) -> Union[User, None]:
        for user in self._users.values():
            if user.id == user_id:
                return user
        return None


def test_register_user_with_valid_data():
    """有効なデータでユーザーを登録できる"""
    # Arrange
    repository = InMemoryUserRepository()
    service = RegistrationService(repository)

    # Act
    user = service.register("test@example.com", "password123")

    # Assert
    assert user.email == "test@example.com"


def test_registered_user_is_saved_to_repository():
    """登録したユーザーがリポジトリに保存される"""
    # Arrange
    repository = InMemoryUserRepository()
    service = RegistrationService(repository)

    # Act
    service.register("test@example.com", "password123")

    # Assert
    saved_user = repository.find_by_email("test@example.com")
    assert saved_user is not None
    assert saved_user.email == "test@example.com"


def test_password_is_hashed_when_registered():
    """登録時にパスワードがハッシュ化される"""
    # Arrange
    repository = InMemoryUserRepository()
    service = RegistrationService(repository)

    # Act
    user = service.register("test@example.com", "password123")

    # Assert
    assert user.hashed_password != "password123"


def test_register_with_duplicate_email_raises_error():
    """既存のメールアドレスで登録するとエラーになる"""
    # Arrange
    repository = InMemoryUserRepository()
    service = RegistrationService(repository)
    service.register("test@example.com", "password123")

    # Act & Assert
    with pytest.raises(ValueError):
        service.register("test@example.com", "another_password")


# RegistrationService プロパティベースドテスト

# テスト用の高速ハッシュ関数（bcryptは遅いのでテストでは使わない）
def fast_hash(password: str) -> str:
    return f"hashed_{password}"


@given(st.emails(), st.text(min_size=8, max_size=100))
def test_any_valid_registration_succeeds(email, password):
    """有効なメールとパスワードなら常に登録できる（プロパティベースド）"""
    repository = InMemoryUserRepository()
    service = RegistrationService(repository, hasher=fast_hash)

    user = service.register(email, password)

    assert user.email is not None  # メールが設定されている
    assert "@" in user.email  # 有効なメール形式
    assert user.hashed_password != password  # ハッシュ化されている


@given(st.emails(), st.text(min_size=8, max_size=100))
def test_registered_user_always_saved_to_repository(email, password):
    """登録されたユーザーは常にリポジトリに保存される（プロパティベースド）"""
    repository = InMemoryUserRepository()
    service = RegistrationService(repository, hasher=fast_hash)

    user = service.register(email, password)

    saved = repository.find_by_email(user.email)  # 正規化後のメールで検索
    assert saved is not None
