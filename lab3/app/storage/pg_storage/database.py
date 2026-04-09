from __future__ import annotations

from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Database:
    _engine = None
    _session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    @classmethod
    async def connect(cls, dsn: str, echo: bool = False) -> None:
        if cls._engine is None:
            cls._engine = create_async_engine(
                dsn,
                echo=echo,
                pool_size=20,
                max_overflow=10,
            )
            cls._session_factory = async_sessionmaker(
                bind=cls._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

    @classmethod
    async def close(cls) -> None:
        if cls._engine is not None:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None

    @classmethod
    def get_session_factory(cls) -> async_sessionmaker[AsyncSession]:
        if cls._session_factory is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls._session_factory

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls._engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_factory = Database.get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
