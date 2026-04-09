from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.user import User, UserModel
from app.storage.repositories import IUserRepository


class PgUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: User) -> User:
        user_orm = UserModel(
            id=uuid.UUID(user.id),
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._session.add(user_orm)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise ValueError(f'Пользователь с логином "{user.login}" уже существует')

        return User(
            id=str(user_orm.id),
            login=user_orm.login,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            email=user_orm.email,
            password_hash=user_orm.password_hash,
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at,
        )

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == uuid.UUID(user_id))
        result = await self._session.execute(stmt)
        user_orm = result.scalar_one_or_none()

        if user_orm is None:
            return None

        return User(
            id=str(user_orm.id),
            login=user_orm.login,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            email=user_orm.email,
            password_hash=user_orm.password_hash,
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at,
        )

    async def get_by_login(self, login: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.login == login)
        result = await self._session.execute(stmt)
        user_orm = result.scalar_one_or_none()

        if user_orm is None:
            return None

        return User(
            id=str(user_orm.id),
            login=user_orm.login,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            email=user_orm.email,
            password_hash=user_orm.password_hash,
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at,
        )

    async def search_by_name_mask(
        self,
        first_name_mask: Optional[str] = None,
        last_name_mask: Optional[str] = None,
    ) -> List[User]:
        conditions = []

        if first_name_mask:
            conditions.append(UserModel.first_name.ilike(f"%{first_name_mask}%"))

        if last_name_mask:
            conditions.append(UserModel.last_name.ilike(f"%{last_name_mask}%"))

        stmt = select(UserModel)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(UserModel.last_name, UserModel.first_name)

        result = await self._session.execute(stmt)
        users_orm = result.scalars().all()

        return [
            User(
                id=str(u.id),
                login=u.login,
                first_name=u.first_name,
                last_name=u.last_name,
                email=u.email,
                password_hash=u.password_hash,
                created_at=u.created_at,
                updated_at=u.updated_at,
            )
            for u in users_orm
        ]
