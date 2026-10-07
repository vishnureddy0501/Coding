# Module 1: FastAPI foundations

This module teaches the smallest complete set of ideas needed to build and reason about a validated HTTP API with FastAPI. It deliberately does **not** cover databases, authentication, dependency injection, middleware, deployment, or detailed asynchronous programming. Those subjects matter, but learning them now would hide the request/response fundamentals.

## Outcome

By the end, you will be able to:

- trace an HTTP request from URL to Python function and back to JSON;
- read FastAPI route signatures without guessing where each value comes from;
- validate path, query, header, and JSON body inputs;
- design separate create, update, and response models with Pydantic;
- use meaningful success and error status codes;
- implement an in-memory CRUD API and explain every important line;
- use `/docs`, `curl`, and `openapi.json` to inspect the API contract.

## How to study this module

Read and run the lessons in order:

1. [Python used by FastAPI](1.python-syntax-for-fastapi.md)
2. [HTTP, the first application, and routes](2.first-application-and-routes.md)
3. [Request inputs](3.request-inputs.md)
4. [Pydantic and response contracts](4.pydantic-models.md)
5. [Build the task API](5.practice.md)
6. [Reference implementation](6.reference-implementation.md)

Do not merely read code. For each example:

1. predict the response;
2. run the request;
3. intentionally send one invalid value;
4. explain why FastAPI accepted or rejected it.

Use the reference implementation only after attempting the capstone yourself.

## Setup

This material assumes Python 3.10 or newer and Pydantic v2 syntax.

```bash
mkdir module-1-project
cd module-1-project
uv init
uv add "fastapi[standard]"
mkdir app
touch app/__init__.py app/main.py
```

Run the application from `module-1-project`:

```bash
uv run fastapi dev app/main.py
```

Important local URLs:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI document: `http://127.0.0.1:8000/openapi.json`

## The mental model to keep

```text
HTTP request
  method + path + query + headers + body
                    |
                    v
           route selection
                    |
                    v
       parsing and input validation
                    |
                    v
          your Python function
                    |
                    v
      response validation/serialization
                    |
                    v
HTTP response
  status code + headers + JSON body
```

FastAPI mainly handles the edges of this flow. Your application function still contains the business decision: what should happen with valid input?

## Scope boundary

After this module, it is normal that you still cannot answer questions about database sessions, `Depends`, JWTs, middleware, or whether a route should use `async def`. Those belong later. In Module 1, ordinary `def` routes and in-memory data let you learn the API contract without unrelated machinery.
