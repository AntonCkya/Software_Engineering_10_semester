from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.parcel import Parcel


class IParcelRepository(ABC):
    @abstractmethod
    def create(self, parcel: Parcel) -> Parcel:
        pass

    @abstractmethod
    def get_by_id(self, parcel_id: str) -> Optional[Parcel]:
        pass

    @abstractmethod
    def get_by_tracking_number(self, tracking_number: str) -> Optional[Parcel]:
        pass

    @abstractmethod
    def get_by_owner_id(self, owner_id: str) -> List[Parcel]:
        pass
