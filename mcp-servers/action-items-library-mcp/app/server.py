from typing import Literal

from mcp.server import MCPServer

from app import repository


mcp = MCPServer("Action Items Library")


@mcp.tool()
async def search_action_items(
    search: str | None = None,
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None,
    limit: int = 20,
) -> dict:
    """Search Action Items Library templates by name and optional priority."""
    safe_limit = max(1, min(limit, 50))
    items = await repository.search(search, priority, safe_limit)
    return {"items": items, "count": len(items)}


@mcp.tool()
async def get_action_item(action_library_id: str) -> dict:
    """Get one Action Items Library template by its exact library ID."""
    item = await repository.get_by_id(action_library_id.strip())
    return {"found": item is not None, "item": item}


@mcp.tool()
async def get_action_item_counts() -> dict[str, int]:
    """Count Action Items Library templates grouped by priority."""
    return await repository.counts_by_priority()


if __name__ == "__main__":
    mcp.run()
