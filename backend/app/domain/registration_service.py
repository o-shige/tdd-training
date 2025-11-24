"""ユーザー登録サービス"""

from typing import Callable

from app.domain.password import hash_password
from app.domain.user import User


class RegistrationService:
    """ユーザー登録のビジネスロジックを担当"""

    def __init__(self, repository, hasher: Callable[[str], str] = hash_password):
        self._repository = repository
        self._hasher = hasher

    def register(self, email: str, password: str) -> User:
        existing = self._repository.find_by_email(email)
        if existing:
            raise ValueError(f"Email {email} is already registered")

        hashed = self._hasher(password)
        user = User(email=email, hashed_password=hashed)
        self._repository.save(user)
        return user
