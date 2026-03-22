from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.auth import decode_token
from app.storage import user_repository
from app.models import User

security = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
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

    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_optional_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[User]:
    if creds is None:
        return None
    try:
        return await get_current_user(creds)
    except HTTPException:
        return None


async def get_current_user_from_refresh_token(
    creds: HTTPAuthorizationCredentials = Depends(security),
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

    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно валидировать авторизационные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
