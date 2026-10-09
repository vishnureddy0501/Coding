from app.action_items_library.models.action_item_library import (
    ActionItemLibraryCreateRequest,
    ActionItemLibraryCreateResponse,
)
from app.action_items_library.persistence.repository import (
    get_action_item_library_repository,
)


async def create_action_item_library(
    data: ActionItemLibraryCreateRequest,
) -> ActionItemLibraryCreateResponse:
    repository = get_action_item_library_repository()
    document = data.model_dump(mode="json")
    result = await repository.create(document)

    return ActionItemLibraryCreateResponse(
        action_library_id=str(result.inserted_id),
        success=result.acknowledged,
    )


def create_action_item_library_bulk(data: list[ActionItemLibraryCreateRequest]):
    print(data)
