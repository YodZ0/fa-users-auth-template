import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.database import db_provider
from src.middleware import apply_middleware
from src.router import apply_routes

from src.tools.database.loaddata import load_data

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Start application")
    await load_data()
    yield
    logger.info("Dispose application")
    await db_provider.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI template",
        lifespan=lifespan,
    )
    app = apply_middleware(app)
    app = apply_routes(app)
    return app
