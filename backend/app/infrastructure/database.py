"""SQLAlchemyデータベース設定

【なぜこのファイルが必要？】
SQLAlchemyでデータベース操作するための基盤設定です。

【Baseクラスとは？】
SQLAlchemyの「宣言的マッピング」で使う基底クラス。
すべてのテーブルクラス（エンティティ）はこのBaseを継承します。

例：
class User(Base):  # ←このBase
    __tablename__ = 'users'
    ...
"""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Boolean, create_engine
import uuid
import os
from datetime import datetime, timezone

# データベース接続URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/auth_db")

# SQLAlchemyエンジン作成
engine = create_engine(DATABASE_URL)

# セッションファクトリー作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# すべてのSQLAlchemyモデルの基底クラス
Base = declarative_base()


class UserModel(Base):
    """ユーザーテーブルのSQLAlchemyモデル

    【なぜドメインのUserクラスと別？】
    - ドメインのUser: ビジネスロジックに特化（バリデーション、計算など）
    - UserModel: データベース操作に特化（テーブル構造、SQL生成など）

    【責任の分離】
    - ドメイン層: 「ユーザーとはこういうもの」
    - インフラ層: 「データベースにはこう保存する」
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)