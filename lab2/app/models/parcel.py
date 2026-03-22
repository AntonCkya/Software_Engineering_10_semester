from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Parcel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: str = ""
    tracking_number: str = ""
    description: str = ""
    weight_kg: float = 0.0
    dimensions: str = ""  # по типу "10x20x30 см".
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
