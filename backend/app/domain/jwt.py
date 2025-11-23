"""JWT生成・検証機能"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
DEFAULT_EXPIRE_MINUTES = 15

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """アクセストークンを生成する"""
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=DEFAULT_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """トークンを検証してペイロードを返す"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("トークンの有効期限が切れています")
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"無効なトークンです: {str(e)}")