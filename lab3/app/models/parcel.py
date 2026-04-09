from dataclasses import dataclass, field
from datetime import datetime
import uuid

from sqlalchemy import String, Numeric, CheckConstraint, Index, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.user import Base


class ParcelModel(Base):
    __tablename__ = "parcels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    tracking_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    weight_kg: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, server_default="0.00"
    )
    dimensions: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=""
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("NOW()"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("NOW()"),
        onupdate=datetime.now,
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("weight_kg >= 0", name="chk_parcels_weight_positive"),
        CheckConstraint(
            "length(trim(tracking_number)) > 0", name="chk_parcels_tracking_not_empty"
        ),
        Index("idx_parcels_owner_id", "owner_id"),
        Index("idx_parcels_tracking_number", "tracking_number"),
    )


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
