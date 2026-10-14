from typing import Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

from app.config import settings


COLLECTION_NAME = "cs_action_items_library"

client = AsyncMongoClient(
    settings.mongo_uri,
    serverSelectionTimeoutMS=5_000,
)
database = client[settings.mongo_database]


def get_action_items_collection() -> AsyncCollection[dict[str, Any]]:
    """Return only the collection that this MCP server is allowed to read."""
    return database.get_collection(COLLECTION_NAME)
