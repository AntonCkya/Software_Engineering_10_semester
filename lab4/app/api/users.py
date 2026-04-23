from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import UserResponse, UserList, UserSearchByMaskRequest
from app.models_mongo import User
from app.storage import MongoUserRepository
from app.api.deps import get_current_user, get_mongo_user_repository

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/login/{login}", response_model=UserResponse)
async def get_user_by_login(
    login: str,
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
):
    user = await user_repo.get_by_login(login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь не найден: "{login}"',
        )

    return UserResponse(
        id=user.id,
        login=user.login,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/search", response_model=UserList)
async def search_users_by_name_mask(
    request: UserSearchByMaskRequest,
    user_repo: MongoUserRepository = Depends(get_mongo_user_repository),
):
    if not request.first_name_mask and not request.last_name_mask:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не передана ни одна маска...",
        )

    users = await user_repo.search_by_name_mask(
        first_name_mask=request.first_name_mask, last_name_mask=request.last_name_mask
    )

    return UserList(
        users=[
            UserResponse(
                id=u.id,
                login=u.login,
                first_name=u.first_name,
                last_name=u.last_name,
                email=u.email,
                created_at=u.created_at,
                updated_at=u.updated_at,
            )
            for u in users
        ],
        total=len(users),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        login=current_user.login,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
