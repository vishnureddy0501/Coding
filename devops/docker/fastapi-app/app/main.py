import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # These values are safe to print and help us understand the active setup.
    logger.info("APP_NAME=%s", settings.app_name)
    logger.info("APP_ENV=%s", settings.app_environment)
    logger.info("DEBUG=%s", settings.debug)
    logger.info("WELCOME_MESSAGE=%s", settings.welcome_message)

    # Never print an actual password, token or connection string.
    secret_status = "configured" if settings.demo_secret != "not-configured" else "missing"
    logger.info("DEMO_SECRET=%s (value hidden)", secret_status)

    yield


app = FastAPI(
    title=settings.app_name,
    description="A small FastAPI application for learning Docker and AWS deployment.",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "app": settings.app_name,
        "environment": settings.app_environment,
        "message": settings.welcome_message,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Docker or AWS can call this endpoint to confirm that the app is alive."""
    return {
        "status": "healthy",
        "environment": settings.app_environment,
    }


@app.get("/api/items/{item_id}")
def get_item(item_id: int) -> dict[str, int | str]:
    return {
        "item_id": item_id,
        "message": f"You requested item {item_id}",
    }
