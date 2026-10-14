# Action Items Library MCP Server

This is a small read-only learning server for `cs_action_items_library`.

## Setup

```bash
cd /Users/aviso/Desktop/Coding/mcp-servers/action-items-library-mcp
cp .env.example .env
```

Fill in `MONGO_URI` and `MONGO_DATABASE`, then run:

```bash
uv sync
uv run mcp dev app/server.py
```

Try these tools in Inspector:

```text
search_action_items(search="kickoff", priority="HIGH", limit=10)
get_action_item(action_library_id="your-id")
get_action_item_counts()
```

## Important

- Use a development database first.
- Use a MongoDB credential with read-only permission.
- The database is fixed through environment configuration.
- The collection is fixed in code.
