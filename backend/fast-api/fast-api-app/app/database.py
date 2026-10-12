from typing import Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from app.config import settings


_client: AsyncMongoClient | None = None
_database: AsyncDatabase[dict[str, Any]] | None = None


async def connect_to_mongodb() -> None:
    global _client, _database

    _client = AsyncMongoClient(
        settings.mongo_url,
        serverSelectionTimeoutMS=5000,
    )

    try:
        await _client.admin.command("ping")
    except Exception:
        await _client.close()
        _client = None
        raise

    _database = _client[settings.mongo_database]


async def close_mongodb_connection() -> None:
    global _client, _database

    if _client is not None:
        await _client.close()

    _client = None
    _database = None


async def check_mongodb_connection() -> None:
    if _client is None:
        raise RuntimeError("MongoDB is not connected")

    await _client.admin.command("ping")


def get_database() -> AsyncDatabase[dict[str, Any]]:
    if _database is None:
        raise RuntimeError("MongoDB is not connected")

    return _database


def get_collection(name: str) -> AsyncCollection[dict[str, Any]]:
    """Return a MongoDB collection from the active application database."""
    return get_database().get_collection(name)
