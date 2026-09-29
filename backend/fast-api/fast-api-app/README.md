# Basic FastAPI practice application

This is intentionally a minimal project. It uses one application file, one test file and temporary in-memory data. There is no database, router structure, repository layer or authentication yet.

## Project structure

```text
fast-api-app/
├── app/
│   ├── __init__.py
│   └── main.py       # settings, schemas, data and endpoints
├── tests/
│   └── test_tasks.py
├── .env              # local settings; ignored by Git
├── .env.example      # safe configuration template
├── pyproject.toml    # dependencies and tool settings
└── uv.lock           # exact dependency versions
```

## 1. Enter the project

```bash
cd /Users/aviso/Desktop/Coding/backend/fast-api/fast-api-app
```

## 2. Install dependencies

```bash
uv sync
```

This creates `.venv` and installs the dependencies. If `.env` is missing, create it from the template:

```bash
cp .env.example .env
```

## 3. Run the development server

```bash
uv run fastapi dev app/main.py
```

Open:

- API documentation: `http://127.0.0.1:8000/docs`
- Application root: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`

Stop the server with `Ctrl+C`.

## 4. Try the API

The easiest method is Swagger UI at `/docs`. You can also use these commands.

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn FastAPI","description":"Practice CRUD"}'
```

List tasks:

```bash
curl http://127.0.0.1:8000/tasks
```

Get, update and delete task `1`:

```bash
curl http://127.0.0.1:8000/tasks/1

curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H 'Content-Type: application/json' \
  -d '{"completed":true}'

curl -X DELETE http://127.0.0.1:8000/tasks/1
```

The data is stored in a Python dictionary. It disappears whenever the server restarts. That is intentional for now.

## 5. Run tests

```bash
uv run pytest
```

Run code-quality checks:

```bash
uv run ruff check app tests
uv run ruff format --check app tests
```

## What to practice first

1. Read `app/main.py` from top to bottom.
2. Create, list, retrieve, update and delete tasks through `/docs`.
3. Try invalid values and inspect the `422` response.
4. Add a `priority` field to the task models.
5. Add a query parameter that filters completed tasks.
6. Add tests for update, delete and pagination.

Keep this version simple until routes, schemas, validation and tests feel comfortable. Add a database and split files only after that.
