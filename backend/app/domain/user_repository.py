"""UserRepositoryインターフェース"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> User | None:
        pass
