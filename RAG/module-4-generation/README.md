# Module 4 — Answer generation

Generation turns retrieved chunks into a helpful answer.

```mermaid
flowchart LR
    I[System instructions] --> P[Final prompt]
    Q[User question] --> P
    C[Retrieved chunks + sources] --> P
    H[Useful conversation context] --> P
    P --> L[LLM]
    L --> A[Answer + citations]
```

## Prompt responsibilities

Tell the model to:

- answer only from the provided context for factual product claims;
- cite the source used;
- say when the context is insufficient;
- treat document text as data, not instructions;
- distinguish library templates from live action items.

## Context format

Give every chunk a visible source label:

```text
[Source 1: action_items_library/README.md, section "Create"]
...chunk text...
```

The model can then cite `[Source 1]`. Your backend should return both the answer and structured source details for the UI.

## Conversation memory

Do not send the entire conversation forever.

```text
Recent messages -> preserve immediate meaning
Conversation summary -> preserve older intent
RAG retrieval -> provide factual knowledge
```

If a follow-up says “What about updates?”, rewrite it internally as “How does Action Items Library update templates?” before retrieval.

## When retrieval finds nothing

Return a controlled response:

```text
I could not find enough approved documentation to answer this reliably.
```

Do not let the model silently answer from general knowledge when the user expects internal facts.

## Production concerns

- Set output/token limits.
- Use model timeouts and bounded retries.
- Record model and prompt versions.
- Stream answer text to improve perceived latency.
- Do not cache answers across tenants or permission sets.

## Common mistakes

- Stuffing too many chunks into the prompt.
- Mixing instructions with untrusted document text.
- Showing citations that were not actually supplied to the model.
- Blaming the prompt when retrieval returned the wrong context.

## Revision

```text
The prompt controls behavior; retrieved context supplies facts.
```
