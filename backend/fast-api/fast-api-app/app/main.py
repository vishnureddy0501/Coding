from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.action_items_library.api.v1.router import router as action_items_library_route
from app.config import settings
from app.database import close_mongodb_connection, connect_to_mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    try:
        yield
    finally:
        await close_mongodb_connection()


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
