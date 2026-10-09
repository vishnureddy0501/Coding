from typing import Any

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import InsertOneResult

from app.database import get_collection


_COLLECTION_NAME = "action_items_library"


class ActionItemLibraryRepository:
    """MongoDB operations for the action-items library collection."""

    def __init__(self, collection: AsyncCollection[dict[str, Any]]) -> None:
        self._collection = collection

    async def create(self, document: dict[str, Any]) -> InsertOneResult:
        return await self._collection.insert_one(document)


def get_action_item_library_repository() -> ActionItemLibraryRepository:
    collection = get_collection(_COLLECTION_NAME)
    return ActionItemLibraryRepository(collection)
