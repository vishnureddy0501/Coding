# FastAPI: half-day interview and development guide

This folder teaches the FastAPI knowledge that gives the highest interview and development value without trying to cover every feature.

For a slower lesson-by-lesson course that also teaches the required Python syntax, start with [`fast-api-learning/plan.md`](fast-api-learning/plan.md).

## Four-hour plan

| Time | Read | Goal |
|---|---|---|
| 0:00–0:40 | `1.fundamentals.md` | Understand requests, routes and automatic docs |
| 0:40–1:20 | `2.validation-and-models.md` | Learn Pydantic and response models |
| 1:20–2:00 | `3.dependencies-errors-middleware.md` | Understand FastAPI's most important abstraction |
| 2:00–2:35 | `4.async-and-database.md` | Avoid blocking and structure database code |
| 2:35–3:05 | `5.authentication-and-security.md` | Explain a secure authentication flow |
| 3:05–3:35 | `6.testing.md` | Write and discuss API tests |
| 3:35–4:00 | `7.production.md` and `8.interview-questions.md` | Revise production and interview topics |

If time is short, read files 1, 2, 3, 4 and 8.

## What “mastery” means for today

After this guide, you should be able to:

- build CRUD endpoints with validated inputs and outputs;
- explain FastAPI, ASGI, Pydantic and Uvicorn;
- use dependency injection for database sessions and authentication;
- choose correctly between `def` and `async def`;
- organize a production application;
- test endpoints and override dependencies;
- discuss authentication, performance and deployment in an interview.

Do not spend today learning WebSockets, custom OpenAPI generation, GraphQL, complex background workers or framework internals.

## Runnable practice application

The [`fast-api-app`](fast-api-app/README.md) folder contains a working FastAPI + MongoDB task API. After studying files 1–8, use its README to run the application and complete the exercises.

The project uses the official asynchronous PyMongo API rather than Motor. All application code, environment files, dependencies and tests are isolated inside that folder.
