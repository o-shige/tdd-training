"""Userドメインエンティティのテスト"""

import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError

from app.domain.user import User


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


def test_user_repository_interface_has_save_method():
    """UserRepositoryインターフェースにsaveメソッドが定義されている"""
    from app.domain.user_repository import UserRepository

    assert hasattr(UserRepository, 'save')


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
