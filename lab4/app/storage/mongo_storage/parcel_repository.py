from __future__ import annotations

from typing import List, Optional

from app.models.parcel_mongo import Parcel
from app.storage.repositories import IParcelRepository

class MongoParcelRepository(IParcelRepository):
    """Репозиторий для работы с посылками в MongoDB"""

    collection_name = "parcels"

    def __init__(self, db):
        self.db = db
        self.collection = db[self.collection_name]

    async def create(self, parcel: Parcel) -> Parcel:
        """Создать новую посылку"""
        doc = parcel.to_mongo()
        result = self.collection.insert_one(doc)
        parcel.id = str(result.inserted_id)
        return parcel

    async def get_by_id(self, parcel_id: str) -> Optional[Parcel]:
        """Получить посылку по ID"""
        doc = self.collection.find_one({"_id": parcel_id})
        if doc:
            return Parcel.from_mongo(doc)
        return None

    async def get_by_tracking_number(self, tracking_number: str) -> Optional[Parcel]:
        """Получить посылку по трек-номеру"""
        doc = self.collection.find_one({"tracking_number": tracking_number})
        if doc:
            return Parcel.from_mongo(doc)
        return None

    async def get_by_owner_id(self, owner_id: str) -> List[Parcel]:
        """Получить все посылки пользователя"""
        docs = self.collection.find({"owner_id": owner_id}).to_list(length=None)
        return [Parcel.from_mongo(doc) for doc in docs]
