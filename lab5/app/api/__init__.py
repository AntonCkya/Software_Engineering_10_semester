from .auth import router as auth_router
from .users import router as users_router
from .parcels import router as parcels_router
from .deliveries import router as deliveries_router

__all__ = ["auth_router", "users_router", "parcels_router", "deliveries_router"]
