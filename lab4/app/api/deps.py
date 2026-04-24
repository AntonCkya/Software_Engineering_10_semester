from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.auth import decode_token
from app.storage import (
    MongoDB,
    MongoUserRepository,
    MongoParcelRepository,
    MongoDeliveryRepository,
)
from app.models.user_mongo import User as MongoUser

security = HTTPBearer()

# MongoDB dependencies
def get_mongo_user_repository():
    db = MongoDB.get_database()
    return MongoUserRepository(db)

def get_mongo_parcel_repository():
    db = MongoDB.get_database()
    return MongoParcelRepository(db)

def get_mongo_delivery_repository():
    db = MongoDB.get_database()
    return MongoDeliveryRepository(db)

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
) -> MongoUser:
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

async def get_current_user_mongo(
    creds: HTTPAuthorizationCredentials = Depends(security),
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
) -> MongoUser:
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
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
) -> Optional[MongoUser]:
    if creds is None:
        return None
    try:
        return await get_current_user(creds, user_repo)
    except HTTPException:
        return None

async def get_current_optional_user_mongo(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
) -> Optional[MongoUser]:
    if creds is None:
        return None
    try:
        return await get_current_user_mongo(creds, user_repo)
    except HTTPException:
        return None

async def get_current_user_from_refresh_token(
    creds: HTTPAuthorizationCredentials = Depends(security),
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
) -> MongoUser:
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
