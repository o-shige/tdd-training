"""SQLAlchemy UserRepository実装のテスト

【このファイルの目的】
UserRepositoryインターフェースをSQLAlchemyで実装したクラスをテストします。

【なぜSQLAlchemyなの？】
SQLAlchemyはPythonで一番よく使われるデータベースライブラリです。
SQLを書かなくても、Pythonのコードでデータベース操作ができます。

【なぜテストでインメモリDBを使う？】
テスト用にPostgreSQLを毎回起動するのは時間がかかります。
SQLiteのインメモリDB（:memory:）を使えば：
- 超高速（0.1秒以下）
- テスト終了時に自動削除される（掃除不要）
- 他のテストと干渉しない
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.user import User
from app.infrastructure.user_repository import SqlAlchemyUserRepository
from app.infrastructure.database import Base


class TestSqlAlchemyUserRepository:
    """SQLAlchemy UserRepository実装のテスト

    【テストの進め方】
    1. 各テストでインメモリDBを作成
    2. テーブルを作成
    3. SqlAlchemyUserRepositoryを作成
    4. テストを実行
    5. テスト終了時に自動でDBが削除される
    """

    @pytest.fixture
    def repository(self):
        """テスト用のSqlAlchemyUserRepositoryを作成

        【@pytest.fixtureとは？】
        テストで共通して使うものを準備する機能。
        各テストメソッドの引数に「repository」と書くだけで使えます。
        """
        # インメモリSQLiteデータベースを作成
        engine = create_engine("sqlite:///:memory:", echo=False)

        # テーブル作成
        Base.metadata.create_all(engine)

        # セッション作成
        Session = sessionmaker(bind=engine)
        session = Session()

        # リポジトリ作成
        repository = SqlAlchemyUserRepository(session)

        return repository

    def test_save_user_should_return_user_with_id(self, repository):
        """ユーザーを保存すると、IDが付与されたユーザーが返される

        【このテストの意図】
        - save()メソッドが正しく動作するか
        - 保存されたユーザーにIDが設定されるか
        """
        # Arrange（準備）
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123"
        )
        original_id = user.id

        # Act（実行）
        saved_user = repository.save(user)

        # Assert（検証）
        assert saved_user is not None
        assert saved_user.id == original_id
        assert saved_user.email == "test@example.com"
        assert saved_user.hashed_password == "hashed_password_123"

    def test_find_by_id_should_return_saved_user(self, repository):
        """IDでユーザーを検索すると、保存したユーザーが返される

        【このテストの意図】
        - save()で保存したデータがDBに保存されているか
        - find_by_id()で正しく取得できるか
        """
        # Arrange（準備）
        user = User(
            email="find_test@example.com",
            hashed_password="hashed_password_456"
        )
        saved_user = repository.save(user)

        # Act（実行）
        found_user = repository.find_by_id(saved_user.id)

        # Assert（検証）
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.email == "find_test@example.com"
        assert found_user.hashed_password == "hashed_password_456"

    def test_find_by_id_should_return_none_when_user_not_exists(self, repository):
        """存在しないIDで検索すると、Noneが返される

        【このテストの意図】
        - データが見つからない場合の処理が正しいか
        - エラーではなくNoneを返すか
        """
        import uuid

        # Arrange（準備）
        non_existent_id = uuid.uuid4()

        # Act（実行）
        found_user = repository.find_by_id(non_existent_id)

        # Assert（検証）
        assert found_user is None

    def test_find_by_email_should_return_saved_user(self, repository):
        """メールアドレスでユーザーを検索すると、保存したユーザーが返される

        【このテストの意図】
        - find_by_email()が正しく動作するか
        - 重複チェックで使用される重要なメソッド
        """
        # Arrange（準備）
        user = User(
            email="email_test@example.com",
            hashed_password="hashed_password_789"
        )
        saved_user = repository.save(user)

        # Act（実行）
        found_user = repository.find_by_email("email_test@example.com")

        # Assert（検証）
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.email == "email_test@example.com"

    def test_find_by_email_should_return_none_when_user_not_exists(self, repository):
        """存在しないメールアドレスで検索すると、Noneが返される

        【このテストの意図】
        - 新規登録時「このメールアドレスは使用可能」の判定で使用
        """
        # Act（実行）
        found_user = repository.find_by_email("nonexistent@example.com")

        # Assert（検証）
        assert found_user is None