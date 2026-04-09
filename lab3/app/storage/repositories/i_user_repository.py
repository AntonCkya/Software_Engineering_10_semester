from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        pass

    @abstractmethod
    def search_by_name_mask(
        self,
        first_name_mask: Optional[str] = None,
        last_name_mask: Optional[str] = None,
    ) -> List[User]:
        pass
