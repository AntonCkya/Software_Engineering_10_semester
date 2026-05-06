from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import String, CheckConstraint, Index, ForeignKey, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.user import Base


class DeliveryModel(Base):
    __tablename__ = "deliveries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    parcel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("parcels.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="pending"
    )
    sender_address: Mapped[str] = mapped_column(
        String, nullable=False, server_default=""
    )
    recipient_address: Mapped[str] = mapped_column(
        String, nullable=False, server_default=""
    )
    estimated_delivery_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    actual_delivery_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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
        CheckConstraint(
            "status IN ('pending', 'in_transit', 'delivered', 'cancelled')",
            name="chk_deliveries_status",
        ),
        CheckConstraint(
            "sender_id != recipient_id", name="chk_deliveries_different_users"
        ),
        Index("idx_deliveries_sender_id", "sender_id"),
        Index("idx_deliveries_recipient_id", "recipient_id"),
        Index("idx_deliveries_parcel_id", "parcel_id"),
        Index("idx_deliveries_status_created", "status", text("created_at DESC")),
    )


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
