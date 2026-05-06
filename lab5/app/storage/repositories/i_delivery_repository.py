from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.delivery import Delivery


class IDeliveryRepository(ABC):
    @abstractmethod
    def create(self, delivery: Delivery) -> Delivery:
        pass

    @abstractmethod
    def get_by_id(self, delivery_id: str) -> Optional[Delivery]:
        pass

    @abstractmethod
    def get_by_sender_id(self, sender_id: str) -> List[Delivery]:
        pass

    @abstractmethod
    def get_by_recipient_id(self, recipient_id: str) -> List[Delivery]:
        pass
