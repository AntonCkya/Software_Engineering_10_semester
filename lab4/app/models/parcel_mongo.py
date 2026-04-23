from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Parcel:
    id: str = ""
    owner_id: str = ""
    tracking_number: str = ""
    description: str = ""
    weight_kg: float = 0.0
    dimensions: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_mongo(doc: dict) -> "Parcel":
        """Создать Parcel из документа MongoDB"""
        return Parcel(
            id=str(doc.get("_id", "")),
            owner_id=str(doc.get("owner_id", "")),
            tracking_number=doc.get("tracking_number", ""),
            description=doc.get("description", ""),
            weight_kg=float(doc.get("weight_kg", 0.0)),
            dimensions=doc.get("dimensions", ""),
            created_at=doc.get("created_at", datetime.now()),
            updated_at=doc.get("updated_at", datetime.now()),
        )

    def to_mongo(self) -> dict:
        result = {
            "owner_id": self.owner_id,
            "tracking_number": self.tracking_number,
            "description": self.description,
            "weight_kg": self.weight_kg,
            "dimensions": self.dimensions,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.id:
            result["_id"] = self.id
        return result

    def update_from_mongo(self, doc: dict) -> None:
        self.id = str(doc.get("_id", ""))
        self.owner_id = str(doc.get("owner_id", ""))
        self.tracking_number = doc.get("tracking_number", "")
        self.description = doc.get("description", "")
        self.weight_kg = float(doc.get("weight_kg", 0.0))
        self.dimensions = doc.get("dimensions", "")
        self.created_at = doc.get("created_at", datetime.now())
        self.updated_at = doc.get("updated_at", datetime.now())
