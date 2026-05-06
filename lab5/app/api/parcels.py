from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import ParcelResponse, ParcelCreate, ParcelList
from app.models import User, Parcel
from app.storage import PgUserRepository, PgParcelRepository
from app.api.deps import get_current_user, get_user_repository, get_parcel_repository

router = APIRouter(prefix="/parcels", tags=["parcels"])


@router.post("", response_model=ParcelResponse, status_code=status.HTTP_201_CREATED)
async def create_parcel(
    request: ParcelCreate,
    current_user: User = Depends(get_current_user),
    user_repo: PgUserRepository = Depends(get_user_repository),
    parcel_repo: PgParcelRepository = Depends(get_parcel_repository),
):
    owner = await user_repo.get_by_id(request.owner_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Отправитель не найден: "{request.owner_id}"',
        )

    parcel = Parcel(
        owner_id=request.owner_id,
        description=request.description,
        weight_kg=request.weight_kg,
        dimensions=request.dimensions,
    )

    db_parcel = await parcel_repo.create(parcel)

    return ParcelResponse(
        id=db_parcel.id,
        owner_id=db_parcel.owner_id,
        tracking_number=db_parcel.tracking_number,
        description=db_parcel.description,
        weight_kg=db_parcel.weight_kg,
        dimensions=db_parcel.dimensions,
        created_at=db_parcel.created_at,
        updated_at=db_parcel.updated_at,
    )


@router.get("/{parcel_id}", response_model=ParcelResponse)
async def get_parcel(
    parcel_id: str,
    current_user: User = Depends(get_current_user),
    parcel_repo: PgParcelRepository = Depends(get_parcel_repository),
):
    parcel = await parcel_repo.get_by_id(parcel_id)
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Посылка не найдена: "{parcel_id}"',
        )

    return ParcelResponse(
        id=parcel.id,
        owner_id=parcel.owner_id,
        tracking_number=parcel.tracking_number,
        description=parcel.description,
        weight_kg=parcel.weight_kg,
        dimensions=parcel.dimensions,
        created_at=parcel.created_at,
        updated_at=parcel.updated_at,
    )


@router.get("/user/{user_id}", response_model=ParcelList)
async def get_user_parcels(
    user_id: str,
    current_user: User = Depends(get_current_user),
    user_repo: PgUserRepository = Depends(get_user_repository),
    parcel_repo: PgParcelRepository = Depends(get_parcel_repository),
):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Отправитель не найден: "{user_id}"',
        )

    parcels = await parcel_repo.get_by_owner_id(user_id)

    return ParcelList(
        parcels=[
            ParcelResponse(
                id=p.id,
                owner_id=p.owner_id,
                tracking_number=p.tracking_number,
                description=p.description,
                weight_kg=p.weight_kg,
                dimensions=p.dimensions,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in parcels
        ],
        total=len(parcels),
    )


@router.get("/tracking/{tracking_number}", response_model=ParcelResponse)
async def get_parcel_by_tracking(
    tracking_number: str,
    current_user: User = Depends(get_current_user),
    parcel_repo: PgParcelRepository = Depends(get_parcel_repository),
):
    parcel = await parcel_repo.get_by_tracking_number(tracking_number)
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Посылка с таким номером не найдена: "{tracking_number}"',
        )

    return ParcelResponse(
        id=parcel.id,
        owner_id=parcel.owner_id,
        tracking_number=parcel.tracking_number,
        description=parcel.description,
        weight_kg=parcel.weight_kg,
        dimensions=parcel.dimensions,
        created_at=parcel.created_at,
        updated_at=parcel.updated_at,
    )
