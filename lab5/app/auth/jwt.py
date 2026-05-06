from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(clear_pass: str, hashed_pass: str) -> bool:
    return crypto_context.verify(clear_pass, hashed_pass)


def get_password_hash(password: str) -> str:
    return crypto_context.hash(password)


def create_access_token(data: dict, user_expires: Optional[timedelta] = None) -> str:
    new_data = data.copy()

    if user_expires:
        expire_at = datetime.now() + user_expires
    else:
        expire_at = datetime.now() + timedelta(
            minutes=settings.auth.access_token_expire_minutes
        )

    new_data.update({"exp": expire_at, "type": "access"})
    jwt_access_token = jwt.encode(
        new_data, settings.auth.jwt_secret_key, algorithm=settings.auth.jwt_algorithm
    )
    return jwt_access_token


def create_refresh_token(data: dict) -> str:
    new_data = data.copy()
    expire_at = datetime.now() + timedelta(days=settings.auth.refresh_token_expire_days)
    new_data.update({"exp": expire_at, "type": "refresh"})

    jwt_refresh_token = jwt.encode(
        new_data, settings.auth.jwt_secret_key, algorithm=settings.auth.jwt_algorithm
    )
    return jwt_refresh_token


def decode_token(token: str, token_type: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.auth.jwt_secret_key,
            algorithms=[settings.auth.jwt_algorithm],
        )
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None
