from typing import Dict, List, Optional

from app.models.delivery import Delivery
from app.storage.repositories import IDeliveryRepository


class DeliveryRepository(IDeliveryRepository):
    def __init__(self):
        self._deliveries: Dict[str, Delivery] = {}

    def create(self, delivery: Delivery) -> Delivery:
        self._deliveries[delivery.id] = delivery
        return delivery

    def get_by_id(self, delivery_id: str) -> Optional[Delivery]:
        return self._deliveries.get(delivery_id)

    def get_by_sender_id(self, sender_id: str) -> List[Delivery]:
        return [d for d in self._deliveries.values() if d.sender_id == sender_id]

    def get_by_recipient_id(self, recipient_id: str) -> List[Delivery]:
        return [d for d in self._deliveries.values() if d.recipient_id == recipient_id]
