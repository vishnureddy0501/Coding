from app.action_items_library.models.action_item_library import (
    ActionItemLibraryCreateRequest,
    ActionItemLibraryCreateResponse,
    ActionItemLibraryUpdateRequest,
    ActionItemLibraryUpdateResponse
)
from app.database import get_collection


async def create_action_item_library(
    data: ActionItemLibraryCreateRequest,
) -> ActionItemLibraryCreateResponse:
    collection = get_collection("action_items_library")
    document = data.model_dump(mode="json")
    result = await collection.insert_one(document)

    return ActionItemLibraryCreateResponse(
        action_library_id=str(result.inserted_id),
        success=result.acknowledged,
    )


async def create_action_item_library_bulk(items: list[ActionItemLibraryCreateRequest]):
    documents = [item.model_dump(exclude_none=True) for item in items]
    if not documents:
        return []
    collection = get_collection("action_items_library")
    result = await collection.insert_many(documents, ordered=True)
    return [str(object_id) for object_id in result.inserted_ids]


async def update_action_item_library(data: ActionItemLibraryUpdateRequest, action_library_id: str):
    collection = get_collection("action_items_library")
    result = collection.update_one(
        {action_library_id},
        {"set": data.model_dump(exclude_unset=True)}
    )
    return ActionItemLibraryUpdateResponse(
        action_library_id=str(result.modified_count),
        success=result.acknowledged,
    )