"""Userドメインエンティティ"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """ユーザーエンティティ"""

    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    hashed_password: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
