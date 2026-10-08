# FastAPI development snippets

These workspace snippets capture the reusable development patterns from the
`customer-success` service without copying its business-specific resources.
They intentionally contain no test snippets.

Open this repository as the VS Code workspace, open a Python file, and type
`fastapi.`. Select a snippet and use `Tab` to move through its placeholders.

## Application structure

```text
fastapi.app
fastapi.app.lifespan
fastapi.router
fastapi.router.include
fastapi.router.feature_include
fastapi.route.feature_router
fastapi.middleware.class
fastapi.middleware.trace
fastapi.middleware.cors
fastapi.health
```

## API routes

```text
fastapi.route.get
fastapi.route.list
fastapi.route.list_body
fastapi.route.post
fastapi.route.put
fastapi.route.patch
fastapi.route.delete
fastapi.route.error_boundary
```

## Models and errors

```text
fastapi.model.request
fastapi.model.update
fastapi.model.strict_update
fastapi.model.response
fastapi.model.list_response
fastapi.model.validator
fastapi.model.root_validator
fastapi.model.factories
fastapi.model.dump_update
fastapi.error.http
fastapi.error.boundary
fastapi.error.validation_handler
```

## Services and MongoDB

```text
fastapi.service.create
fastapi.service.list
fastapi.service.gather
fastapi.service.search_filter
fastapi.service.log
fastapi.mongo.collection
fastapi.mongo.find_one
fastapi.mongo.page
fastapi.mongo.update
fastapi.mongo.soft_delete
fastapi.mongo.update_many
fastapi.mongo.aggregate
fastapi.mongo.indexes
fastapi.mongo.error.duplicate
fastapi.mongo.error.operation
```

## Utilities

```text
fastapi.config.settings
fastapi.time.utc
fastapi.logger
fastapi.task.create
fastapi.middleware.register
```

## Conventions captured

- Keep endpoint modules thin and delegate business logic to services.
- Preserve `HTTPException`; log unexpected failures and return a safe 500.
- Resolve collections by tenant and exclude soft-deleted documents by default.
- Fetch `limit + 1` documents when a response needs `has_more`.
- Escape user input before building a MongoDB regex.
- Use `model_dump(exclude_unset=True)` for partial updates.
- Use `Field(default_factory=...)` for mutable or nested defaults.
- Create indexes from actual filter and sort patterns during onboarding.

The reference service exposes synchronous PyMongo-style collection operations
from async service functions. If a new project uses an async MongoDB driver,
add `await` consistently across that entire data-access path.
