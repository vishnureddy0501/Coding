from enum import Enum

from pydantic import BaseModel, Field


class PriorityValue(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ActionItemLibraryCreateRequest(BaseModel):
    action_name: str = Field(
        description="Enter action item name",
        min_length=5,
        max_length=20,
    )
    description: str = Field(
        description="Enter description",
        min_length=5,
        max_length=20,
    )
    priority: PriorityValue = PriorityValue.LOW


class ActionItemLibraryCreateResponse(BaseModel):
    action_library_id: str
    success: bool    