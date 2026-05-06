from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import auth_router, users_router, parcels_router, deliveries_router
from app.config import settings
from app.storage import Database
from app.rate_limit import rate_limiter


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

    @app.on_event("startup")
    async def startup():
        await Database.connect(
            dsn=settings.database.dsn,
            echo=settings.server.debug,
        )

    @app.on_event("shutdown")
    async def shutdown():
        await Database.close()

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        if request.url.path in ["/", "/health"]:
            return await call_next(request)

        if request.url.path.startswith("/api/v1/auth"):
            if request.url.path in ["/api/v1/auth/register", "/api/v1/auth/login"]:
                client_ip = request.headers.get("X-Forwarded-For", request.client.host)
                if "," in client_ip:
                    client_ip = client_ip.split(",")[0].strip()

                endpoint = request.url.path

                if request.url.path == "/api/v1/auth/register":
                    allowed, remaining, reset = rate_limiter.check_sliding_window(
                        identifier=client_ip,
                        endpoint=endpoint,
                        limit=settings.rate_limit.register_limit,
                        window_size=settings.rate_limit.register_window
                    )
                    limit_value = settings.rate_limit.register_limit
                else:
                    allowed, remaining, reset = rate_limiter.check_sliding_window(
                        identifier=client_ip,
                        endpoint=endpoint,
                        limit=settings.rate_limit.login_limit,
                        window_size=settings.rate_limit.login_window
                    )
                    limit_value = settings.rate_limit.login_limit

                response = Response()
                response.headers["X-RateLimit-Limit"] = str(limit_value)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Reset"] = str(reset)

                if not allowed:
                    response = Response(
                        content="{\"detail\": \"Слишком много запросов. Попробуйте позже.\"}",
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        media_type="application/json"
                    )
                    response.headers["Retry-After"] = str(reset)
                    return response

        response = await call_next(request)

        if hasattr(response, "headers"):
            if "X-RateLimit-Limit" not in response.headers:
                response.headers["X-RateLimit-Limit"] = "unlimited"
                response.headers["X-RateLimit-Remaining"] = "unlimited"
                response.headers["X-RateLimit-Reset"] = "0"
                
        return response

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
