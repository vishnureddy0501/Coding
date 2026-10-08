# Module 2: Build a safe data-access layer

The chatbot must not receive a database connection, arbitrary SQL, arbitrary MongoDB filters, or unrestricted API access.

Instead, application code exposes a few approved read functions:

```text
chatbot orchestration
    → get_account(context, account_id)
    → list_open_tickets(context, account_id, limit)
    → get_account_health(context, account_id)
```

Each function decides the query, allowed fields, permission filters, and result limit. The model will only be allowed to request these operations in Module 3.

## Outcome

After this module, you should understand how to:

- carry trusted tenant and user information in `RequestContext`;
- expose narrow read functions instead of raw database access;
- enforce tenant and record permissions in every operation;
- return only approved fields through Pydantic models;
- wrap an existing internal API behind the same boundary;
- distinguish missing data, forbidden data, and temporary failures internally;
- give the public chatbot a safe result without leaking record existence.

## Lessons

1. [Trusted context and public data models](1.context-and-models.md)
2. [Safe database reads](2.database-reads.md)
3. [Safe internal API reads](3.api-reads.md)
4. [Service boundary and failure handling](4.service-boundary.md)
5. [Module practice](5.practice.md)
6. [Reference implementation](6.reference-implementation.md)

## Request flow

```text
authenticated FastAPI request
    → build trusted RequestContext
    → call one approved data function
    → enforce tenant + user access
    → select approved fields and limit rows
    → validate the result with Pydantic
    → return evidence to later chatbot layers
```

## Out of scope

This module does not add an LLM, tool calling, RAG, embeddings, conversation memory, write operations, or testing.
