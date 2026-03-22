from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


class DeliveryStatus:
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Delivery:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
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
