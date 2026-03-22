from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class DeliveryCreate(BaseModel):
    sender_id: str = Field(...)
    recipient_id: str = Field(...)
    parcel_id: str = Field(...)
    sender_address: str = Field(..., min_length=1, max_length=500)
    recipient_address: str = Field(..., min_length=1, max_length=500)
    estimated_delivery_date: Optional[datetime] = Field(None)


class DeliveryResponse(BaseModel):
    id: str
    sender_id: str
    recipient_id: str
    parcel_id: str
    status: str
    sender_address: str
    recipient_address: str
    estimated_delivery_date: Optional[datetime]
    actual_delivery_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class DeliveryList(BaseModel):
    deliveries: List[DeliveryResponse]
    total: int
