from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.delivery import Delivery, DeliveryModel
from app.storage.repositories import IDeliveryRepository


class PgDeliveryRepository(IDeliveryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, delivery: Delivery) -> Delivery:
        delivery_orm = DeliveryModel(
            id=uuid.UUID(delivery.id),
            sender_id=uuid.UUID(delivery.sender_id),
            recipient_id=uuid.UUID(delivery.recipient_id),
            parcel_id=uuid.UUID(delivery.parcel_id),
            status=delivery.status,
            sender_address=delivery.sender_address,
            recipient_address=delivery.recipient_address,
            estimated_delivery_date=delivery.estimated_delivery_date,
            actual_delivery_date=delivery.actual_delivery_date,
            created_at=delivery.created_at,
            updated_at=delivery.updated_at,
        )
        self._session.add(delivery_orm)
        await self._session.commit()

        return Delivery(
            id=str(delivery_orm.id),
            sender_id=str(delivery_orm.sender_id),
            recipient_id=str(delivery_orm.recipient_id),
            parcel_id=str(delivery_orm.parcel_id),
            status=delivery_orm.status,
            sender_address=delivery_orm.sender_address,
            recipient_address=delivery_orm.recipient_address,
            estimated_delivery_date=delivery_orm.estimated_delivery_date,
            actual_delivery_date=delivery_orm.actual_delivery_date,
            created_at=delivery_orm.created_at,
            updated_at=delivery_orm.updated_at,
        )

    async def get_by_id(self, delivery_id: str) -> Optional[Delivery]:
        stmt = select(DeliveryModel).where(DeliveryModel.id == uuid.UUID(delivery_id))
        result = await self._session.execute(stmt)
        delivery_orm = result.scalar_one_or_none()

        if delivery_orm is None:
            return None

        return Delivery(
            id=str(delivery_orm.id),
            sender_id=str(delivery_orm.sender_id),
            recipient_id=str(delivery_orm.recipient_id),
            parcel_id=str(delivery_orm.parcel_id),
            status=delivery_orm.status,
            sender_address=delivery_orm.sender_address,
            recipient_address=delivery_orm.recipient_address,
            estimated_delivery_date=delivery_orm.estimated_delivery_date,
            actual_delivery_date=delivery_orm.actual_delivery_date,
            created_at=delivery_orm.created_at,
            updated_at=delivery_orm.updated_at,
        )

    async def get_by_sender_id(self, sender_id: str) -> List[Delivery]:
        stmt = (
            select(DeliveryModel)
            .where(DeliveryModel.sender_id == uuid.UUID(sender_id))
            .order_by(DeliveryModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        deliveries_orm = result.scalars().all()

        return [
            Delivery(
                id=str(d.id),
                sender_id=str(d.sender_id),
                recipient_id=str(d.recipient_id),
                parcel_id=str(d.parcel_id),
                status=d.status,
                sender_address=d.sender_address,
                recipient_address=d.recipient_address,
                estimated_delivery_date=d.estimated_delivery_date,
                actual_delivery_date=d.actual_delivery_date,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in deliveries_orm
        ]

    async def get_by_recipient_id(self, recipient_id: str) -> List[Delivery]:
        stmt = (
            select(DeliveryModel)
            .where(DeliveryModel.recipient_id == uuid.UUID(recipient_id))
            .order_by(DeliveryModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        deliveries_orm = result.scalars().all()

        return [
            Delivery(
                id=str(d.id),
                sender_id=str(d.sender_id),
                recipient_id=str(d.recipient_id),
                parcel_id=str(d.parcel_id),
                status=d.status,
                sender_address=d.sender_address,
                recipient_address=d.recipient_address,
                estimated_delivery_date=d.estimated_delivery_date,
                actual_delivery_date=d.actual_delivery_date,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in deliveries_orm
        ]
