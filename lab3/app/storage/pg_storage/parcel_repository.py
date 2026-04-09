from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parcel import Parcel, ParcelModel
from app.storage.repositories import IParcelRepository


class PgParcelRepository(IParcelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, parcel: Parcel) -> Parcel:
        tracking_number = self._generate_tracking_number()

        parcel_orm = ParcelModel(
            id=uuid.UUID(parcel.id),
            owner_id=uuid.UUID(parcel.owner_id),
            tracking_number=tracking_number,
            description=parcel.description,
            weight_kg=parcel.weight_kg,
            dimensions=parcel.dimensions,
            created_at=parcel.created_at,
            updated_at=parcel.updated_at,
        )
        self._session.add(parcel_orm)
        await self._session.commit()

        return Parcel(
            id=str(parcel_orm.id),
            owner_id=str(parcel_orm.owner_id),
            tracking_number=parcel_orm.tracking_number,
            description=parcel_orm.description,
            weight_kg=float(parcel_orm.weight_kg),
            dimensions=parcel_orm.dimensions,
            created_at=parcel_orm.created_at,
            updated_at=parcel_orm.updated_at,
        )

    async def get_by_id(self, parcel_id: str) -> Optional[Parcel]:
        stmt = select(ParcelModel).where(ParcelModel.id == uuid.UUID(parcel_id))
        result = await self._session.execute(stmt)
        parcel_orm = result.scalar_one_or_none()

        if parcel_orm is None:
            return None

        return Parcel(
            id=str(parcel_orm.id),
            owner_id=str(parcel_orm.owner_id),
            tracking_number=parcel_orm.tracking_number,
            description=parcel_orm.description,
            weight_kg=float(parcel_orm.weight_kg),
            dimensions=parcel_orm.dimensions,
            created_at=parcel_orm.created_at,
            updated_at=parcel_orm.updated_at,
        )

    async def get_by_tracking_number(self, tracking_number: str) -> Optional[Parcel]:
        stmt = select(ParcelModel).where(ParcelModel.tracking_number == tracking_number)
        result = await self._session.execute(stmt)
        parcel_orm = result.scalar_one_or_none()

        if parcel_orm is None:
            return None

        return Parcel(
            id=str(parcel_orm.id),
            owner_id=str(parcel_orm.owner_id),
            tracking_number=parcel_orm.tracking_number,
            description=parcel_orm.description,
            weight_kg=float(parcel_orm.weight_kg),
            dimensions=parcel_orm.dimensions,
            created_at=parcel_orm.created_at,
            updated_at=parcel_orm.updated_at,
        )

    async def get_by_owner_id(self, owner_id: str) -> List[Parcel]:
        stmt = (
            select(ParcelModel)
            .where(ParcelModel.owner_id == uuid.UUID(owner_id))
            .order_by(ParcelModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        parcels_orm = result.scalars().all()

        return [
            Parcel(
                id=str(p.id),
                owner_id=str(p.owner_id),
                tracking_number=p.tracking_number,
                description=p.description,
                weight_kg=float(p.weight_kg),
                dimensions=p.dimensions,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in parcels_orm
        ]

    @staticmethod
    def _generate_tracking_number() -> str:
        return f"TRK{uuid.uuid4().hex[:12].upper()}"
