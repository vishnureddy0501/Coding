# Module 5: FastAPI chat orchestration

Assemble the live-data chatbot behind one endpoint:

```text
POST /api/v1/chat
→ build authenticated RequestContext
→ scope classification
→ approved tool calling
→ live database/API result
→ evidence-based answer
→ validated ChatResponse
```

## Lessons

1. [API contract and trusted context](1.api-contract.md)
2. [Orchestration and failures](2.orchestration.md)
3. [Reference implementation](3.reference-implementation.md)
4. [Practice](4.practice.md)

The route contains no database queries, prompts, or authorization rules.
