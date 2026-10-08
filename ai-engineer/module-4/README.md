# Module 4: Scope classification and refusal

The chatbot supports only live project-data operations:

```text
get_account
list_open_tickets
get_account_health
```

Before calling a tool, classify the question into one of these intents or reject it.

## Lessons

1. [Layered scope gate](1.scope-gate.md)
2. [Structured classification and routing](2.classification.md)
3. [Reference implementation](3.reference-implementation.md)
4. [Practice](4.practice.md)

## Outcomes

```text
supported + complete arguments → run approved tool
supported + missing account   → needs_clarification
supported + missing data      → no_information
unsupported question          → out_of_scope
dependency failure            → temporarily_unavailable
```

Document search and RAG are deliberately deferred.
