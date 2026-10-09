from fastapi import APIRouter

from app.action_items_library.api.v1.action_items_library import (
    router as action_items_library_router,
)


router = APIRouter()
router.include_router(
    action_items_library_router,
    prefix="/action-items-library",
    tags=["Action Items Library"],
)
