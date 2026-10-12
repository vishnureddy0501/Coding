import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from app.action_items_library.api.v1.router import router as action_items_library_route
from app.config import settings
from app.database import (
    check_mongodb_connection,
    close_mongodb_connection,
    connect_to_mongodb,
)


logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings.validate_runtime()
    try:
        await connect_to_mongodb()
        logger.info("Application started in %s mode", settings.app_env)
        yield
    finally:
        await close_mongodb_connection()
        logger.info("Application stopped")


app = FastAPI(
    title=settings.app_name,
    docs_url="/docs",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(action_items_library_route)


@app.get("/")
async def root():
    return {"message": settings.app_name}


@app.get("/health")
async def health():
    return {"status": "ok", "environment": settings.app_env}


@app.get("/ready")
async def readiness():
    try:
        await check_mongodb_connection()
    except Exception as error:
        logger.exception("Readiness check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="A required dependency is unavailable",
        ) from error

    return {"status": "ready"}
