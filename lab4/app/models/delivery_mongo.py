from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

class DeliveryStatus:
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Delivery:
    id: str = ""
    sender_id: str = ""
    recipient_id: str = ""
    parcel_id: str = ""
    status: str = DeliveryStatus.PENDING
    sender_address: str = ""
    recipient_address: str = ""
    estimated_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_mongo(doc: dict) -> "Delivery":
        return Delivery(
            id=str(doc.get("_id", "")),
            sender_id=str(doc.get("sender_id", "")),
            recipient_id=str(doc.get("recipient_id", "")),
            parcel_id=str(doc.get("parcel_id", "")),
            status=doc.get("status", DeliveryStatus.PENDING),
            sender_address=doc.get("sender_address", ""),
            recipient_address=doc.get("recipient_address", ""),
            estimated_delivery_date=doc.get("estimated_delivery_date"),
            actual_delivery_date=doc.get("actual_delivery_date"),
            created_at=doc.get("created_at", datetime.now()),
            updated_at=doc.get("updated_at", datetime.now()),
        )

    def to_mongo(self) -> dict:
        result = {
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "parcel_id": self.parcel_id,
            "status": self.status,
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.estimated_delivery_date:
            result["estimated_delivery_date"] = self.estimated_delivery_date
        if self.actual_delivery_date:
            result["actual_delivery_date"] = self.actual_delivery_date
        if self.id:
            result["_id"] = self.id
        return result

    def update_from_mongo(self, doc: dict) -> None:
        self.id = str(doc.get("_id", ""))
        self.sender_id = str(doc.get("sender_id", ""))
        self.recipient_id = str(doc.get("recipient_id", ""))
        self.parcel_id = str(doc.get("parcel_id", ""))
        self.status = doc.get("status", DeliveryStatus.PENDING)
        self.sender_address = doc.get("sender_address", "")
        self.recipient_address = doc.get("recipient_address", "")
        self.estimated_delivery_date = doc.get("estimated_delivery_date")
        self.actual_delivery_date = doc.get("actual_delivery_date")
        self.created_at = doc.get("created_at", datetime.now())
        self.updated_at = doc.get("updated_at", datetime.now())
