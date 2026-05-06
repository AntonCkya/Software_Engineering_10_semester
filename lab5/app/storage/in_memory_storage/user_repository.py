from typing import Dict, List, Optional
import fnmatch

from app.models.user import User
from app.storage.repositories import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._login_index: Dict[str, str] = {}

    def create(self, user: User) -> User:
        if user.login in self._login_index:
            raise ValueError(f'Пользователь с логином "{user.login}" уже существует')
        self._users[user.id] = user
        self._login_index[user.login] = user.id
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_by_login(self, login: str) -> Optional[User]:
        user_id = self._login_index.get(login)
        if user_id:
            return self._users.get(user_id)
        return None

    def search_by_name_mask(
        self,
        first_name_mask: Optional[str] = None,
        last_name_mask: Optional[str] = None,
    ) -> List[User]:
        results = []
        for user in self._users.values():
            match = True
            if first_name_mask:
                if not fnmatch.fnmatch(
                    user.first_name.lower(), first_name_mask.lower()
                ):
                    match = False
            if last_name_mask:
                if not fnmatch.fnmatch(user.last_name.lower(), last_name_mask.lower()):
                    match = False
            if match:
                results.append(user)
        return results
