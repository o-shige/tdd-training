"""SQLAlchemy UserRepository実装

【このファイルの目的】
UserRepositoryインターフェースをSQLAlchemyで実装します。

【実装のポイント】
1. ドメインのUserオブジェクト ⇔ SQLAlchemyのUserModel の変換
2. データベースセッション管理
3. エラーハンドリング
"""

from uuid import UUID, uuid4
from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.user import User
from app.domain.user_repository import UserRepository
from app.infrastructure.database import UserModel


class SqlAlchemyUserRepository(UserRepository):
    """SQLAlchemyを使ったUserRepository実装

    【なぜセッションを受け取る？】
    データベース接続（セッション）は外部から注入します。
    - テスト時: インメモリDB用セッション
    - 本番時: PostgreSQL用セッション
    同じコードで異なるDBを使い分けられます。

    【変換処理】
    ドメインUser ←→ SQLAlchemyUserModel の相互変換を行います。
    """

    def __init__(self, session: Session):
        self._session = session

    def save(self, user: User) -> User:
        """ユーザーをデータベースに保存

        【処理の流れ】
        1. ドメインUser → SQLAlchemyUserModel に変換
        2. データベースに保存
        3. SQLAlchemyUserModel → ドメインUser に変換して返却
        """
        # ドメインモデルからデータベースモデルに変換
        user_model = UserModel(
            id=str(user.id),  # UUID → 文字列に変換
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            is_active=user.is_active
        )

        try:
            # データベースに保存
            self._session.add(user_model)
            self._session.commit()
            self._session.refresh(user_model)  # IDなど自動生成値を取得

            # データベースモデルからドメインモデルに変換して返却
            return self._to_domain_user(user_model)

        except IntegrityError:
            # 重複エラーなど制約違反の場合
            self._session.rollback()
            raise

    def find_by_id(self, id: UUID) -> Union[User, None]:
        """IDでユーザーを検索

        【処理の流れ】
        1. SQLAlchemyでデータベース検索
        2. 見つかったらドメインUserに変換
        3. 見つからなければNoneを返却
        """
        user_model = self._session.query(UserModel).filter(UserModel.id == str(id)).first()

        if user_model is None:
            return None

        return self._to_domain_user(user_model)

    def find_by_email(self, email: str) -> Union[User, None]:
        """メールアドレスでユーザーを検索

        【なぜemailで検索？】
        ユーザー登録時の重複チェックで使用します。
        「このメールアドレスは既に登録済みです」の判定。
        """
        user_model = self._session.query(UserModel).filter(UserModel.email == email).first()

        if user_model is None:
            return None

        return self._to_domain_user(user_model)

    def _to_domain_user(self, user_model: UserModel) -> User:
        """SQLAlchemyモデルをドメインモデルに変換

        【なぜ変換が必要？】
        - データベース層とドメイン層の責任を分離
        - SQLAlchemyの内部実装をドメインに漏れさせない
        - テストしやすさを向上
        """
        return User(
            id=UUID(user_model.id),  # 文字列 → UUIDに変換
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            created_at=user_model.created_at,
            is_active=user_model.is_active
        )