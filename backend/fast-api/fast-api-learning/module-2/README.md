# Module 2: Production structure used in `customer-success`

Module 1 covered FastAPI's input boundary. This module now follows the patterns that are actually present in the senior-written `customer-success` project.

## Outcome

After this module, you should be able to:

- raise `HTTPException` without losing known business errors;
- register the project's custom `RequestValidationError` handler;
- compose paths through nested `APIRouter`s;
- keep API functions thin and call async service functions;
- read lifespan startup/shutdown and middleware flow;
- build a small feature using the same API/model/service layout.

## Lessons

1. [Responses and status codes](1.responses-and-status-codes.md)
2. [Errors used in customer-success](2.errors-and-exception-handlers.md)
3. [How routers and service functions work together](3.dependency-injection.md)
4. [Application lifespan and middleware](4.dependency-lifecycle.md)
6. [Module 2 capstone](6.practice.md)
7. [Reference implementation](7.reference-implementation.md)

## Study method

Trace one request through the same layers as the project:

```text
middleware
    ↓
router + request validation
    ↓
API function
    ↓
service function
    ↓
response model
```

For each code sample, identify which layer receives the request, which layer contains business logic, and which layer creates the response.

## Deliberately out of scope

The reference project does not use `Depends`, sub-dependencies, dependency caching, or yield dependencies, so Module 2 does not teach them.
