# FastAPI learning plan

Use this folder as both a learning course and an interview revision guide. Study the lessons in order because later lessons assume that earlier concepts are clear.

## How to study each lesson

For every lesson:

1. Read the explanation once.
2. Type the examples yourself instead of copying them.
3. Change one or two values and predict the result.
4. Complete the exercises without looking at the answer.
5. Explain the lesson aloud in simple words.

Do not try to memorize every function. Understand what FastAPI is doing with normal Python types and functions.

## Module 1 — Foundation

Goal: understand the Python syntax FastAPI uses and build a small validated API.

- [Lesson 1: Python syntax required for FastAPI](module-1/1.python-syntax-for-fastapi.md)
- [Lesson 2: First application and routes](module-1/2.first-application-and-routes.md)
- [Lesson 3: Path, query, header and body inputs](module-1/3.request-inputs.md)
- [Lesson 4: Pydantic models and validation](module-1/4.pydantic-models.md)
- [Lesson 5: Module 1 practice](module-1/5.practice.md)

After Module 1, you should be able to build a small in-memory CRUD API and explain automatic validation and documentation.

## Module 2 — Responses, errors and dependency injection

Goal: build cleaner endpoints with predictable responses and reusable request logic.

- Response models and safe output
- HTTP status codes and `Response`
- `HTTPException`
- Custom exception handlers
- Python syntax: function objects, callables and `Annotated`
- `Depends` from first principles
- Nested dependencies and dependency caching
- Dependencies using `yield`
- Dependency overrides in tests

## Module 3 — Application structure and middleware

Goal: organize a growing FastAPI service without creating unnecessary complexity.

- `APIRouter`
- Python modules, packages and imports
- Separating routes, schemas and services
- Configuration and `.env` files
- Middleware execution flow
- CORS
- Request state and request IDs
- Lifespan startup and shutdown

## Module 4 — Async and database development

Goal: understand concurrency and connect an API to a real database safely.

- Python `async def`, `await` and coroutines
- I/O-bound versus CPU-bound work
- Blocking calls inside async endpoints
- Database session/client dependencies
- CRUD with a database
- Transactions and indexes
- Pagination
- Migrations for relational databases
- MongoDB document concepts if MongoDB is selected

Learn one database path first. Do not try to learn SQLAlchemy and MongoDB simultaneously.

## Module 5 — Authentication and security

Goal: protect endpoints and explain production API security.

- Authentication versus authorization
- Bearer-token extraction
- Password hashing
- JWT structure and validation
- Current-user dependency
- Roles, permissions and resource ownership
- Cookies, sessions and CSRF
- CORS versus authentication
- Secrets and environment configuration
- Rate limiting and common API-security mistakes

## Module 6 — Testing and production

Goal: test confidently and understand how a FastAPI application is deployed.

- Pytest fundamentals
- `TestClient`
- Fixtures
- Dependency overrides and mocks
- Unit versus integration tests
- Testing validation and authorization
- Uvicorn and ASGI workers
- Containers and environment configuration
- Health checks
- Logging, metrics and tracing
- Timeouts, retries and background jobs
- Final interview revision

## Recommended order

Complete one module before moving to the next:

```text
Python and FastAPI basics
        ↓
Responses, errors and dependencies
        ↓
Project structure and middleware
        ↓
Async and database
        ↓
Authentication and security
        ↓
Testing and production
```

## Topics to postpone

These are useful but not required at the beginning:

- WebSockets
- GraphQL
- custom OpenAPI generation
- advanced Pydantic core schemas
- advanced validator `plain` and `wrap` modes
- distributed background-task systems
- writing a custom authentication provider

