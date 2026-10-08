# Module 3: Tool calling for structured and live data

Module 2 created three safe operations:

```text
get_account
list_open_tickets
get_account_health
```

Module 3 lets the model request one of those operations. The model never executes code or receives database connections, API credentials, tenant selection, or arbitrary query access.

## Outcome

After this module, you should understand how to:

- describe approved operations as function tools;
- keep trusted context out of model-generated arguments;
- validate every tool call with Pydantic;
- execute only functions present in an application allow-list;
- return tool results to the model as untrusted evidence;
- limit a question to at most two tool calls;
- generate an answer using only tool evidence.

## Lessons

1. [Tool schemas and arguments](1.tool-schemas.md)
2. [Tool registry and safe execution](2.tool-execution.md)
3. [The tool-calling loop](3.tool-calling-loop.md)
4. [Grounded answers and failures](4.grounded-answers.md)
5. [Module practice](5.practice.md)
6. [Reference implementation](6.reference-implementation.md)

## Complete flow

```text
approved user question
    → model proposes an approved tool and arguments
    → application checks tool name
    → Pydantic validates arguments
    → application injects trusted RequestContext
    → Module 2 service executes the operation
    → application returns structured evidence to the model
    → model answers only from that evidence
```

The model proposes. Your application validates and executes.

## Scope boundary

This module handles structured/live data tools only. Module 4 adds scope classification, and Module 5 adds the FastAPI chat endpoint. Document RAG is deferred.
