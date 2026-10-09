from fastapi import APIRouter, status

from app.action_items_library.models.action_item_library import (
    ActionItemLibraryCreateRequest,
    ActionItemLibraryCreateResponse,
    ActionItemLibraryUpdateRequest,
    ActionItemLibraryUpdateResponse
)
from app.action_items_library.services.action_items_library import (
    create_action_item_library as create_action_item_library_service,
    create_action_item_library_bulk as create_action_item_library_bulk_service,
    update_action_item_library as update_action_item_library_service
)


router = APIRouter()


@router.post(
    "/create",
    response_model=ActionItemLibraryCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_action_item_library(
    body: ActionItemLibraryCreateRequest,
) -> ActionItemLibraryCreateResponse:
    return await create_action_item_library_service(body)

@router.post("/create-bulk")
async def create_action_item_library_bulk(body: list[ActionItemLibraryCreateRequest]):
    return await create_action_item_library_bulk_service(body);


@router.post(
    "/update/{action_library_id}",
    response_model=ActionItemLibraryCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_action_item_library(
    body: ActionItemLibraryUpdateRequest,
    action_library_id: str
) -> ActionItemLibraryCreateResponse:
    return await update_action_item_library_service(body, action_library_id)