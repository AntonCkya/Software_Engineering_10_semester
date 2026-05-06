from fastapi import APIRouter, HTTPException, status, Depends, Request, Response

from app.schemas import (
    Token,
    LoginRequest,
    RegisterRequest,
    UserResponse,
    RefreshTokenRequest,
)
from app.models import User
from app.storage import PgUserRepository
from app.api.deps import get_user_repository
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.rate_limit import rate_limiter
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest,
    user_repo: PgUserRepository = Depends(get_user_repository),
):
    check_user = await user_repo.get_by_login(request.login)
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой пользователь уже существует",
        )

    new_user = User(
        login=request.login,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=get_password_hash(request.password),
    )

    try:
        db_user = await user_repo.create(new_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return UserResponse(
        id=db_user.id,
        login=db_user.login,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    user_repo: PgUserRepository = Depends(get_user_repository),
):
    user = await user_repo.get_by_login(request.login)

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id, "login": user.login})
    refresh_token = create_refresh_token(data={"sub": user.id, "login": user.login})

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    user_repo: PgUserRepository = Depends(get_user_repository),
    response: Response = None,
):
    token_data = decode_token(request.refresh_token, "refresh")

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный refresh токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = token_data.get("sub")
    login = token_data.get("login")

    if user_id is None or login is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный refresh токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    allowed, remaining, reset = rate_limiter.check_token_bucket(
        identifier=user_id,
        endpoint="/auth/refresh",
        capacity=settings.rate_limit.refresh_capacity,
        refill_rate=settings.rate_limit.refresh_refill_rate
    )

    if response:
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit.refresh_capacity)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много запросов обновления токена. Попробуйте позже.",
            headers={"Retry-After": str(reset)}
        )

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_access_token = create_access_token(data={"sub": user.id, "login": user.login})
    new_refresh_token = create_refresh_token(data={"sub": user.id, "login": user.login})

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
