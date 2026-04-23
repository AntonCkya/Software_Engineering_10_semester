from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import DeliveryResponse, DeliveryCreate, DeliveryList
from app.models import User, Delivery, DeliveryStatus
from app.storage import PgUserRepository, PgParcelRepository, PgDeliveryRepository
from app.api.deps import (
    get_current_user,
    get_user_repository,
    get_parcel_repository,
    get_delivery_repository,
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.post("", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(
    request: DeliveryCreate,
    current_user: User = Depends(get_current_user),
    user_repo: PgUserRepository = Depends(get_user_repository),
    parcel_repo: PgParcelRepository = Depends(get_parcel_repository),
    delivery_repo: PgDeliveryRepository = Depends(get_delivery_repository),
):
    if request.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя создать доставку от имени другого пользователя",
        )

    sender = await user_repo.get_by_id(request.sender_id)
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Отправитель не найден: "{request.sender_id}"',
        )

    recipient = await user_repo.get_by_id(request.recipient_id)
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Получатель не найден не найден: "{request.recipient_id}"',
        )

    parcel = await parcel_repo.get_by_id(request.parcel_id)
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Посылка не найдена: "{request.parcel_id}"',
        )

    if parcel.owner_id != request.sender_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отправитель не является владельцем посылки",
        )

    delivery = Delivery(
        sender_id=request.sender_id,
        recipient_id=request.recipient_id,
        parcel_id=request.parcel_id,
        sender_address=request.sender_address,
        recipient_address=request.recipient_address,
        estimated_delivery_date=request.estimated_delivery_date,
        status=DeliveryStatus.PENDING,
    )

    db_delivery = await delivery_repo.create(delivery)

    return DeliveryResponse(
        id=db_delivery.id,
        sender_id=db_delivery.sender_id,
        recipient_id=db_delivery.recipient_id,
        parcel_id=db_delivery.parcel_id,
        status=db_delivery.status,
        sender_address=db_delivery.sender_address,
        recipient_address=db_delivery.recipient_address,
        estimated_delivery_date=db_delivery.estimated_delivery_date,
        actual_delivery_date=db_delivery.actual_delivery_date,
        created_at=db_delivery.created_at,
        updated_at=db_delivery.updated_at,
    )


@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(
    delivery_id: str,
    current_user: User = Depends(get_current_user),
    delivery_repo: PgDeliveryRepository = Depends(get_delivery_repository),
):
    delivery = await delivery_repo.get_by_id(delivery_id)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Доставка не найдена"
        )

    return DeliveryResponse(
        id=delivery.id,
        sender_id=delivery.sender_id,
        recipient_id=delivery.recipient_id,
        parcel_id=delivery.parcel_id,
        status=delivery.status,
        sender_address=delivery.sender_address,
        recipient_address=delivery.recipient_address,
        estimated_delivery_date=delivery.estimated_delivery_date,
        actual_delivery_date=delivery.actual_delivery_date,
        created_at=delivery.created_at,
        updated_at=delivery.updated_at,
    )


@router.get("/sender/{sender_id}", response_model=DeliveryList)
async def get_deliveries_by_sender(
    sender_id: str,
    current_user: User = Depends(get_current_user),
    user_repo: PgUserRepository = Depends(get_user_repository),
    delivery_repo: PgDeliveryRepository = Depends(get_delivery_repository),
):
    sender = await user_repo.get_by_id(sender_id)
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Отправитель не найден: "{sender_id}"',
        )

    deliveries = await delivery_repo.get_by_sender_id(sender_id)

    return DeliveryList(
        deliveries=[
            DeliveryResponse(
                id=d.id,
                sender_id=d.sender_id,
                recipient_id=d.recipient_id,
                parcel_id=d.parcel_id,
                status=d.status,
                sender_address=d.sender_address,
                recipient_address=d.recipient_address,
                estimated_delivery_date=d.estimated_delivery_date,
                actual_delivery_date=d.actual_delivery_date,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in deliveries
        ],
        total=len(deliveries),
    )


@router.get("/recipient/{recipient_id}", response_model=DeliveryList)
async def get_deliveries_by_recipient(
    recipient_id: str,
    current_user: User = Depends(get_current_user),
    user_repo: PgUserRepository = Depends(get_user_repository),
    delivery_repo: PgDeliveryRepository = Depends(get_delivery_repository),
):
    recipient = await user_repo.get_by_id(recipient_id)
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Получатель не найден не найден: "{recipient_id}"',
        )

    deliveries = await delivery_repo.get_by_recipient_id(recipient_id)

    return DeliveryList(
        deliveries=[
            DeliveryResponse(
                id=d.id,
                sender_id=d.sender_id,
                recipient_id=d.recipient_id,
                parcel_id=d.parcel_id,
                status=d.status,
                sender_address=d.sender_address,
                recipient_address=d.recipient_address,
                estimated_delivery_date=d.estimated_delivery_date,
                actual_delivery_date=d.actual_delivery_date,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in deliveries
        ],
        total=len(deliveries),
    )
