from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class ParcelCreate(BaseModel):
    owner_id: str = Field(...)
    description: str = Field(..., min_length=1, max_length=500)
    weight_kg: float = Field(..., gt=0, le=10000)
    dimensions: str = Field(..., max_length=50)


class ParcelResponse(BaseModel):
    id: str
    owner_id: str
    tracking_number: str
    description: str
    weight_kg: float
    dimensions: str
    created_at: datetime
    updated_at: datetime


class ParcelList(BaseModel):
    parcels: List[ParcelResponse]
    total: int
