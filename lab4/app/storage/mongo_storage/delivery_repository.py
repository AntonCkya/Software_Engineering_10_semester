from __future__ import annotations

from typing import List, Optional

from app.models.delivery_mongo import Delivery
from app.storage.repositories import IDeliveryRepository

class MongoDeliveryRepository(IDeliveryRepository):
    """Репозиторий для работы с доставками в MongoDB"""

    collection_name = "deliveries"

    def __init__(self, db):
        self.db = db
        self.collection = db[self.collection_name]

    async def create(self, delivery: Delivery) -> Delivery:
        """Создать новую доставку"""
        doc = delivery.to_mongo()
        result = await self.collection.insert_one(doc)
        delivery.id = str(result.inserted_id)
        return delivery

    async def get_by_id(self, delivery_id: str) -> Optional[Delivery]:
        """Получить доставку по ID"""
        doc = await self.collection.find_one({"_id": delivery_id})
        if doc:
            return Delivery.from_mongo(doc)
        return None

    async def get_by_sender_id(self, sender_id: str) -> List[Delivery]:
        """Получить все доставки отправителя"""
        docs = await self.collection.find({"sender_id": sender_id}).to_list(length=None)
        return [Delivery.from_mongo(doc) for doc in docs]

    async def get_by_recipient_id(self, recipient_id: str) -> List[Delivery]:
        """Получить все доставки получателя"""
        docs = await self.collection.find({"recipient_id": recipient_id}).to_list(length=None)
        return [Delivery.from_mongo(doc) for doc in docs]
