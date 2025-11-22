"""パスワードハッシュ化モジュール"""

import bcrypt


def hash_password(password: str) -> bytes:
    """パスワードをハッシュ化する"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """パスワードを検証する"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed)
