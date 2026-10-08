# Generative AI Engineer Plan: Live Project-Data Chatbot

## Single goal

Build a chatbot that:

- answers questions using only approved live database and internal API data;
- respects tenant, user, role, and record permissions;
- refuses unrelated questions and unsupported operations;
- refuses when authorized live data is unavailable or insufficient;
- never invents database values;
- identifies the approved operation used for each answer;
- is exposed through a reliable FastAPI endpoint.

This curriculum is intentionally limited to that goal.

## Deferred topics

Learn these only after the live-data chatbot works:

- document parsing and ingestion;
- RAG over documents;
- embeddings and vector databases;
- document chunking and citations;
- fine-tuning and model training;
- image, audio, and video generation;
- autonomous or multi-agent systems;
- write/update/delete operations through AI.

## Architecture

```text
authenticated user question
        ↓
build trusted tenant/user context
        ↓
scope classifier
        ├── unsupported → out_of_scope
        ├── missing account → needs_clarification
        └── supported live-data intent
                    ↓
model proposes one approved read tool
                    ↓
application validates tool name and arguments
                    ↓
application injects trusted RequestContext
                    ↓
authorized database/API read
                    ↓
evidence status
        ├── missing/unauthorized → no_information
        ├── dependency failure  → temporarily_unavailable
        └── found               → grounded answer + tool source
```

The model never receives a raw database connection, arbitrary query execution, tenant selection, credentials, or arbitrary URL access.

## Initial supported operations

```text
get_account(account_id)
list_open_tickets(account_id, limit)
get_account_health(account_id)
```

Keep the first version read-only.

---

## Module 1 — Define the exact scope

Goal: define users, permissions, entities, fields, supported questions, and refusal behavior before model code.

- [Module 1 guide](module-1/README.md)
- [System boundary](module-1/1.system-boundary.md)
- [Data inventory and permissions](module-1/2.data-inventory.md)
- [Supported intents](module-1/3.supported-intents.md)
- [Refusal behavior](module-1/4.refusal-behavior.md)
- [Practice](module-1/5.practice.md)
- [Scope template](module-1/scope-template.md)
- [Question-set template](module-1/question-set-template.jsonl)

Important outcomes:

```text
answered
needs_clarification
no_information
out_of_scope
temporarily_unavailable
```

---

## Module 2 — Build the safe data-access layer

Goal: expose only narrow, authorized, bounded database/API reads.

- [Module 2 guide](module-2/README.md)
- [Trusted context and public models](module-2/1.context-and-models.md)
- [Safe database reads](module-2/2.database-reads.md)
- [Safe internal API reads](module-2/3.api-reads.md)
- [Service boundary and failures](module-2/4.service-boundary.md)
- [Practice](module-2/5.practice.md)
- [Reference implementation](module-2/6.reference-implementation.md)

Each operation must:

- receive trusted `RequestContext`;
- enforce tenant and account access;
- use a predefined query/API call;
- select only approved fields;
- enforce hard result limits;
- return `found`, `not_found`, or `unavailable`;
- perform no write.

---

## Module 3 — Use tool calling for live data

Goal: allow the model to propose one approved operation without giving it system access.

- [Module 3 guide](module-3/README.md)
- [Tool schemas and arguments](module-3/1.tool-schemas.md)
- [Tool registry and execution](module-3/2.tool-execution.md)
- [Tool-calling loop](module-3/3.tool-calling-loop.md)
- [Grounded answers and failures](module-3/4.grounded-answers.md)
- [Practice](module-3/5.practice.md)
- [Reference implementation](module-3/6.reference-implementation.md)

```text
model proposes
→ application validates
→ application injects context
→ Module 2 service executes
→ model receives approved evidence
→ grounded answer
```

Maximum tool calls per question: two.

---

## Module 4 — Scope classification and refusal

Goal: reject unrelated, incomplete, and unsupported questions before tool execution.

- [Module 4 guide](module-4/README.md)
- [Layered scope gate](module-4/1.scope-gate.md)
- [Structured classification](module-4/2.classification.md)
- [Reference implementation](module-4/3.reference-implementation.md)
- [Practice](module-4/4.practice.md)

The classifier selects only among:

```text
get_account
list_open_tickets
get_account_health
```

It does not answer, authorize records, select tenants, or execute tools.

---

## Module 5 — FastAPI chat orchestration

Goal: assemble trusted context, scope checking, tool calling, live evidence, and public responses.

- [Module 5 guide](module-5/README.md)
- [API contract and trusted context](module-5/1.api-contract.md)
- [Orchestration and failures](module-5/2.orchestration.md)
- [Reference implementation](module-5/3.reference-implementation.md)
- [Practice](module-5/4.practice.md)

Endpoint:

```text
POST /api/v1/chat
```

The request contains the question and optional conversation ID. Tenant, user, role, and account permissions come only from authenticated application context.

---

## Module 6 — Multi-step questions and conversation

Goal: support two approved reads and follow-up questions without using stale facts.

- [Module 6 guide](module-6/README.md)
- [Multi-tool questions](module-6/1.multi-tool-questions.md)
- [Conversation context](module-6/2.conversation-context.md)
- [Reference implementation](module-6/3.reference-implementation.md)
- [Practice](module-6/4.practice.md)

History may resolve “it” to the last selected account. Every factual response still performs a fresh authorized database/API read.

---

## Module 7 — Evaluate the chatbot

Goal: verify scope decisions, tool selection, arguments, authorization, evidence, and answers.

- [Module 7 guide](module-7/README.md)
- [Evaluation cases](module-7/1.cases.md)
- [Metrics and failure analysis](module-7/2.metrics.md)
- [Minimal runner](module-7/3.reference-implementation.md)
- [Practice](module-7/4.practice.md)

Important risks:

```text
false acceptance
false refusal
wrong tool or arguments
unsupported factual claim
authorization leakage
stale conversational answer
```

---

## Module 8 — Production readiness

Goal: deploy a secure, observable, bounded, read-only chatbot.

- [Module 8 guide](module-8/README.md)
- [Security and privacy](module-8/1.security.md)
- [Reliability and observability](module-8/2.reliability.md)
- [Deployment reference](module-8/3.deployment.md)
- [Interview explanation and checklist](module-8/4.interview-and-checklist.md)

Production requirements include authentication, permission enforcement, field/result limits, timeouts, concurrency limits, structured logs, configuration, version tracking, and a safe disable switch.

---

## Final project structure

```text
app/
├── main.py
├── chat/
│   ├── api/v1/chat.py
│   ├── models.py
│   └── orchestrator.py
├── ai/
│   ├── client.py
│   ├── scope.py
│   ├── tool_loop.py
│   └── prompts.py
├── chat_data/
│   ├── context.py
│   ├── models.py
│   ├── repository.py
│   ├── api_client.py
│   └── service.py
├── conversations/
│   └── store.py
└── evaluation/
    ├── cases.jsonl
    └── run_evaluation.py
```

## Interview questions

You should be able to answer:

1. Why not give the LLM direct database access?
2. How is tenant isolation enforced?
3. What is the difference between scope classification and authorization?
4. Why are tool arguments validated again in application code?
5. What is the difference between `out_of_scope` and `no_information`?
6. How do you prevent answers from using outside knowledge?
7. How do follow-up questions retrieve fresh data?
8. How are unauthorized and nonexistent records handled safely?
9. How do you investigate an incorrect answer?
10. What would be required before enabling write operations?

## Definition of done

- Exactly three read intents are supported.
- All operations are allow-listed and bounded.
- Tenant/user permissions are enforced outside the model.
- Every factual answer comes from current database/API evidence.
- Missing/unauthorized data returns `no_information`.
- Unrelated/write requests return `out_of_scope`.
- Failures return `temporarily_unavailable`.
- Sources identify executed tools and entity IDs.
- Follow-ups perform fresh reads.
- Evaluation covers authorization and injection attempts.
- Production timeouts, logs, and limits are configured.

Document RAG can be added later as a separate retrieval path after this project is stable.
