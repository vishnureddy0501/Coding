import re
from typing import Any

from app.database import get_action_items_collection


PUBLIC_FIELDS = {
    "_id": 0,
    "action_library_id": 1,
    "action_name": 1,
    "description": 1,
    "priority": 1,
    "created_by": 1,
    "created_at": 1,
    "last_updated_by": 1,
    "last_updated_at": 1,
}


async def search(
    search_text: str | None,
    priority: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    query: dict[str, Any] = {}

    if search_text:
        query["action_name"] = {
            "$regex": re.escape(search_text.strip()),
            "$options": "i",
        }
    if priority:
        query["priority"] = priority

    cursor = (
        get_action_items_collection()
        .find(query, PUBLIC_FIELDS)
        .sort("last_updated", -1)
        .limit(limit)
    )
    return await cursor.to_list(length=limit)


async def get_by_id(action_library_id: str) -> dict[str, Any] | None:
    return await get_action_items_collection().find_one(
        {"action_library_id": action_library_id},
        PUBLIC_FIELDS,
    )


async def counts_by_priority() -> dict[str, int]:
    pipeline = [
        {"$group": {"_id": "$priority", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "priority": "$_id", "count": 1}},
    ]
    cursor = await get_action_items_collection().aggregate(pipeline)
    rows = await cursor.to_list(length=10)
    counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for row in rows:
        priority = row.get("priority")
        if priority in counts:
            counts[priority] = row["count"]
    return counts
