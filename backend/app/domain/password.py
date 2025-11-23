"""パスワードハッシュ化モジュール"""
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """パスワードをハッシュ化する

    Args:
        password: 平文パスワード

    Returns:
        ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """パスワードを検証する

    Args:
        password: 平文パスワード
        hashed: ハッシュ化されたパスワード

    Returns:
        検証結果
    """
    return pwd_context.verify(password, hashed)
