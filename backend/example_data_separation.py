"""データ保存の役割分担例

【SQLAlchemy vs Redis の使い分け】
このファイルは説明用のサンプルコードです。
実際の実装時の参考にしてください。
"""

# ============================================
# 1. SQLAlchemy (永続データ) - PostgreSQL
# ============================================

from app.infrastructure.user_repository import SqlAlchemyUserRepository
from app.domain.user import User
from datetime import datetime, timedelta
import json

def get_postgresql_session():
    """PostgreSQL セッション取得 (実装例)"""
    # 実際の実装時に置き換え
    pass

def save_user_permanently(user: User):
    """ユーザー情報を永続保存 (PostgreSQL)

    【なぜSQLAlchemy？】
    - ユーザー情報は絶対に消えてはいけない
    - 検索やソートが必要
    - トランザクション管理が必要
    """
    db_session = get_postgresql_session()
    repository = SqlAlchemyUserRepository(db_session)
    return repository.save(user)


# ============================================
# 2. Redis (一時データ) - メモリ管理
# ============================================

try:
    import redis
except ImportError:
    # テスト環境用のモック
    class MockRedis:
        def __init__(self, **kwargs):
            self.data = {}
        def setex(self, key, time, value):
            self.data[key] = value
        def get(self, key):
            return self.data.get(key)
    redis = type('redis', (), {'Redis': MockRedis})

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def save_user_session(user_id: str, session_data: dict):
    """ユーザーセッションを一時保存 (Redis)

    【なぜRedis？】
    - ログイン状態は一時的（ログアウトで消える）
    - 高速アクセスが必要
    - 自動期限切れが便利（TTL）
    """
    session_key = f"session:{user_id}"
    # 24時間で自動削除
    redis_client.setex(
        session_key,
        timedelta(hours=24),
        json.dumps(session_data)
    )

def get_user_session(user_id: str) -> dict:
    """セッション取得"""
    session_key = f"session:{user_id}"
    data = redis_client.get(session_key)
    return json.loads(data) if data else None


# ============================================
# 3. 実際の使用例 - 両方を組み合わせ
# ============================================

class AuthenticationError(Exception):
    """認証エラー"""
    pass

def verify_password(password: str, hashed_password: str) -> bool:
    """パスワード検証 (実装例)"""
    # 実際の実装時に置き換え
    return True

def generate_jwt_token(user_id) -> str:
    """JWTトークン生成 (実装例)"""
    # 実際の実装時に置き換え
    return f"jwt_token_{user_id}"

def login_user(email: str, password: str):
    """ログイン処理 - SQLAlchemy + Redis"""

    # 1. ユーザー認証 (PostgreSQL から検索)
    db_session = get_postgresql_session()
    repository = SqlAlchemyUserRepository(db_session)
    user = repository.find_by_email(email)

    if not user or not verify_password(password, user.hashed_password):
        raise AuthenticationError("Invalid credentials")

    # 2. セッション作成 (Redis に保存)
    session_data = {
        "user_id": str(user.id),
        "email": user.email,
        "login_time": datetime.utcnow().isoformat()
    }
    save_user_session(str(user.id), session_data)

    return generate_jwt_token(user.id)


# ============================================
# 4. テスト環境での違い
# ============================================

def get_test_environment():
    """テスト環境設定"""
    return {
        "database": "sqlite:///:memory:",  # SQLAlchemy + SQLite
        "redis": "fakeredis",              # Redis モック
    }

def get_production_environment():
    """本番環境設定"""
    return {
        "database": "postgresql://user:pass@db:5432/app",  # SQLAlchemy + PostgreSQL
        "redis": "redis://redis:6379",                     # 本物の Redis
    }


# ============================================
# 5. 重要な区別
# ============================================

"""
【SQLAlchemy が扱うもの】
✅ User (ユーザー情報)
✅ Order (注文履歴)
✅ Product (商品情報)
❌ Session (セッション) → Redisが担当

【Redis が扱うもの】
✅ Session (ログイン状態)
✅ Cache (キャッシュデータ)
✅ Rate limiting (API制限)
❌ User data (ユーザー情報) → SQLAlchemyが担当
"""