from .repositories import (
    IUserRepository,
    IParcelRepository,
    IDeliveryRepository,
)
from .in_memory_storage.user_repository import UserRepository
from .in_memory_storage.parcel_repository import ParcelRepository
from .in_memory_storage.delivery_repository import DeliveryRepository
from .pg_storage import (
    Database,
    PgUserRepository,
    PgParcelRepository,
    PgDeliveryRepository,
)
from app.cache.cache_fabric import make_cached_repository

CachedPgUserRepository = make_cached_repository(
    PgUserRepository,
    {
        'get_by_id': {'maxsize': 100, 'ttl': 60}, # частый запрос, данные почти не меняются
        'search_by_name_mask': {'maxsize': 1000, 'ttl': 300} # нечастый запрос, при этом довольно трудоемкий
    }
)

CachedPgParcelRepository = make_cached_repository(
    PgParcelRepository,
    {
        'get_by_id': {'maxsize': 100, 'ttl': 60}, # частый запрос, данные меняются редко
        'get_by_tracking_number': {'maxsize': 100, 'ttl': 60} # частый запрос, данные меняются редко
    }
)

__all__ = [
    "IUserRepository",
    "IParcelRepository",
    "IDeliveryRepository",
    "UserRepository",
    "ParcelRepository",
    "DeliveryRepository",
    "Database",
    "PgUserRepository",
    "PgParcelRepository",
    "PgDeliveryRepository",
    "CachedPgUserRepository",
    "CachedPgParcelRepository",
]
