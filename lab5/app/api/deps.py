from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.auth import decode_token
from app.storage import PgUserRepository, PgParcelRepository, PgDeliveryRepository
from app.storage.pg_storage.database import get_db
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()


def get_user_repository(session: AsyncSession = Depends(get_db)) -> PgUserRepository:
    return PgUserRepository(session)


def get_parcel_repository(
    session: AsyncSession = Depends(get_db),
) -> PgParcelRepository:
    return PgParcelRepository(session)


def get_delivery_repository(
    session: AsyncSession = Depends(get_db),
) -> PgDeliveryRepository:
    return PgDeliveryRepository(session)


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    user_repo: PgUserRepository = Depends(get_user_repository),
) -> User:
    token_data = decode_token(creds.credentials, "access")
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = token_data.get("sub")
    login: str = token_data.get("login")

    if user_id is None or login is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_optional_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
    user_repo: PgUserRepository = Depends(get_user_repository),
) -> Optional[User]:
    if creds is None:
        return None
    try:
        return await get_current_user(creds, user_repo)
    except HTTPException:
        return None


async def get_current_user_from_refresh_token(
    creds: HTTPAuthorizationCredentials = Depends(security),
    user_repo: PgUserRepository = Depends(get_user_repository),
) -> User:
    token_data = decode_token(creds.credentials, "access")
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = token_data.get("sub")
    login: str = token_data.get("login")

    if user_id is None or login is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
