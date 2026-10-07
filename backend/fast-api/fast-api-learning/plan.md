## Module 1 — Foundation

Goal: understand the Python syntax FastAPI uses and build a small validated API.

- [Lesson 1: Python syntax required for FastAPI](module-1/1.python-syntax-for-fastapi.md)
- [Lesson 2: First application and routes](module-1/2.first-application-and-routes.md)
- [Lesson 3: Path, query, header and body inputs](module-1/3.request-inputs.md)
- [Lesson 4: Pydantic models and validation](module-1/4.pydantic-models.md)
- [Lesson 5: Module 1 practice](module-1/5.practice.md)

After Module 1, you should be able to build a small in-memory CRUD API and explain automatic validation and documentation.

## Module 2 — Responses, errors and application flow

Goal: build predictable endpoints and understand the request/application lifecycle used by the reference service.

- [Module 2 guide](module-2/README.md)
- [Lesson 1: Responses and status codes](module-2/1.responses-and-status-codes.md)
- [Lesson 2: Errors and exception handlers](module-2/2.errors-and-exception-handlers.md)
- [Lesson 3: Routers and service functions](module-2/3.dependency-injection.md)
- [Lesson 4: Application lifespan and middleware](module-2/4.dependency-lifecycle.md)
- [Lesson 6: Module 2 practice](module-2/6.practice.md)
- [Reference implementation](module-2/7.reference-implementation.md)

## Module 3 — Application structure

Goal: organize a growing FastAPI service without creating unnecessary complexity.

- [Module 3 guide](module-3/README.md)
- [Packages and imports](module-3/1.packages-and-imports.md)
- [Feature-based application layers](module-3/2.application-layers.md)
- [Router composition](module-3/3.router-composition.md)
- [Configuration and environment variables](module-3/4.configuration.md)
- [Practice](module-3/5.practice.md)

## Module 4 — Async code and MongoDB data access

Goal: understand concurrency and connect an API to a real database safely.

- [Module 4 guide](module-4/README.md)
- [Coroutines, `async def`, and `await`](module-4/1.async-and-await.md)
- [Blocking work](module-4/2.blocking-work.md)
- [MongoDB documents and CRUD](module-4/3.mongodb-crud.md)
- [Filtering, sorting, and pagination](module-4/4.querying-and-pagination.md)
- [Connections, caching, and concurrency safety](module-4/5.connections-and-cache.md)
- [Practice](module-4/6.practice.md)

## Module 5 — Service authentication and security

Goal: protect endpoints and explain production API security.

- [Module 5 guide](module-5/README.md)
- [Authentication, authorization, and trust boundaries](module-5/1.security-foundations.md)
- [Signed internal requests](module-5/2.signed-requests.md)
- [Authentication middleware](module-5/3.auth-middleware.md)
- [CORS, secrets, and safe errors](module-5/4.security-practices.md)
- [Practice](module-5/5.practice.md)

## Module 6 — Production operation

Goal: understand how a FastAPI application is run and observed in production. Testing is deferred.

- [Module 6 guide](module-6/README.md)
- [ASGI, Uvicorn, and containers](module-6/1.asgi-and-containers.md)
- [Health checks and graceful lifecycle](module-6/2.health-and-lifecycle.md)
- [Logging and tracing](module-6/3.observability.md)
- [Timeouts, retries, and background refresh](module-6/4.resilience.md)
- [Production checklist](module-6/5.production-checklist.md)

## Module 7 — Background, scheduled, and bulk-sync jobs

Goal: run work outside the request lifecycle safely and make important jobs durable and resumable.

- [Module 7 guide](module-7-jobs/README.md)
- [Choose the correct job type](module-7-jobs/1.job-types.md)
- [Scheduled email design](module-7-jobs/2.scheduled-email-design.md)
- [Scheduled email implementation](module-7-jobs/3.scheduled-email-implementation.md)
- [Bulk CRM sync design](module-7-jobs/4.bulk-sync-design.md)
- [Bulk CRM sync implementation](module-7-jobs/5.bulk-sync-implementation.md)
- [Running and operating jobs](module-7-jobs/6.running-jobs.md)

## Recommended order

Complete one module before moving to the next:

```text
Python and FastAPI basics
        ↓
Responses, errors and application flow
        ↓
Project structure and middleware
        ↓
Async and database
        ↓
Service authentication and security
        ↓
Production operation
        ↓
Background and bulk jobs
```

## Topics to postpone

These are useful but not required at the beginning:

- WebSockets
- GraphQL
- custom OpenAPI generation
- advanced Pydantic core schemas
- advanced validator `plain` and `wrap` modes
- distributed job frameworks such as Celery
- writing a custom authentication provider
- automated testing (reserved for a later module)
- SQLAlchemy and relational migrations
- browser login, JWT issuance, and session authentication
