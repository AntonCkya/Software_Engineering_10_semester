from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import auth_router, users_router, parcels_router, deliveries_router
from app.config import settings


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        docs_url=settings.app.docs_url,
        redoc_url=settings.app.redoc_url,
        openapi_url=settings.app.openapi_url,
        debug=settings.server.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.cors_allow_origins,
        allow_credentials=settings.app.cors_allow_credentials,
        allow_methods=settings.app.cors_allow_methods,
        allow_headers=settings.app.cors_allow_headers,
    )

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(parcels_router, prefix="/api/v1")
    app.include_router(deliveries_router, prefix="/api/v1")

    return app


app = create_application()


@app.get("/", tags=["root"])
async def root():
    return {
        "name": settings.app.name,
        "version": settings.app.version,
        "environment": settings.environment,
        "docs": settings.app.docs_url,
        "redoc": settings.app.redoc_url,
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": settings.app.version,
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        workers=settings.server.workers,
    )
