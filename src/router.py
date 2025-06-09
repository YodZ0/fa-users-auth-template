from fastapi import FastAPI, APIRouter
from src.apps.healthcheck.router import router as healthcheck_router
from src.apps.auth.router import router as auth_router
from src.apps.users.router import router as users_router
from src.apps.references.router import router as references_router
from src.settings import settings


def apply_routes(app: FastAPI) -> FastAPI:
    # Create main router
    router = APIRouter(prefix=settings.api.prefix)
    # Include API routers
    router.include_router(healthcheck_router)
    router.include_router(auth_router)
    router.include_router(users_router)
    router.include_router(references_router)
    # Include main router
    app.include_router(router)
    return app
