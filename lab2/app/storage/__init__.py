from .repositories import (
    IUserRepository,
    IParcelRepository,
    IDeliveryRepository,
)
from .in_memory_storage.user_repository import UserRepository
from .in_memory_storage.parcel_repository import ParcelRepository
from .in_memory_storage.delivery_repository import DeliveryRepository

# "базы данных", в 3 лабе будут pg репы
user_repository = UserRepository()
parcel_repository = ParcelRepository()
delivery_repository = DeliveryRepository()

__all__ = [
    "IUserRepository",
    "IParcelRepository",
    "IDeliveryRepository",
    "UserRepository",
    "ParcelRepository",
    "DeliveryRepository",
    "user_repository",
    "parcel_repository",
    "delivery_repository",
]
