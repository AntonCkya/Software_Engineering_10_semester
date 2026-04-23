from __future__ import annotations

from typing import List, Optional, Any

from app.models_mongo import User
from app.storage.repositories import IUserRepository

class MongoUserRepository(IUserRepository):
    """Репозиторий для работы с пользователями в MongoDB"""

    collection_name = "users"

    def __init__(self, db: Any):
        self.db = db
        self.collection = db[self.collection_name]

    async def create(self, user: User) -> User:
        """Создать нового пользователя"""
        doc = user.to_mongo()
        result = await self.collection.insert_one(doc)
        user.id = str(result.inserted_id)
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Получить пользователя по ID"""
        doc = await self.collection.find_one({"_id": user_id})
        if doc:
            return User.from_mongo(doc)
        return None

    async def get_by_login(self, login: str) -> Optional[User]:
        """Получить пользователя по логину"""
        doc = await self.collection.find_one({"login": login})
        if doc:
            return User.from_mongo(doc)
        return None

    async def search_by_name_mask(
        self,
        first_name_mask: Optional[str] = None,
        last_name_mask: Optional[str] = None,
    ) -> List[User]:
        """Поиск пользователей по маске имени и фамилии"""
        query = {}
        conditions = []

        if first_name_mask:
            conditions.append({"first_name": {"$regex": first_name_mask, "$options": "i"}})

        if last_name_mask:
            conditions.append({"last_name": {"$regex": last_name_mask, "$options": "i"}})

        if len(conditions) == 1:
            query = conditions[0]
        elif len(conditions) == 2:
            query = {"$and": conditions}

        docs = await self.collection.find(query).sort([("last_name", 1), ("first_name", 1)]).to_list(length=None)
        return [User.from_mongo(doc) for doc in docs]
