from typing import Dict, List, Optional
import uuid

from app.models.parcel import Parcel
from app.storage.repositories import IParcelRepository


class ParcelRepository(IParcelRepository):
    def __init__(self):
        self._parcels: Dict[str, Parcel] = {}
        self._tracking_index: Dict[str, str] = {}

    def _generate_tracking_number(self) -> str:
        return f"TRK{uuid.uuid4().hex[:12].upper()}"

    def create(self, parcel: Parcel) -> Parcel:
        parcel.tracking_number = self._generate_tracking_number()
        self._parcels[parcel.id] = parcel
        self._tracking_index[parcel.tracking_number] = parcel.id
        return parcel

    def get_by_id(self, parcel_id: str) -> Optional[Parcel]:
        return self._parcels.get(parcel_id)

    def get_by_tracking_number(self, tracking_number: str) -> Optional[Parcel]:
        parcel_id = self._tracking_index.get(tracking_number)
        if parcel_id:
            return self._parcels.get(parcel_id)
        return None

    def get_by_owner_id(self, owner_id: str) -> List[Parcel]:
        return [p for p in self._parcels.values() if p.owner_id == owner_id]
