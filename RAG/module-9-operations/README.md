# Module 9 — Monitoring, security, and cost

## Observe one request end to end

Give every question a `request_id` and trace:

```text
authentication
-> query processing
-> embedding
-> vector search
-> reranking
-> LLM generation
-> response
```

## Useful metrics

```text
request count and error rate
p50/p95 total latency
embedding, retrieval, reranking and LLM latency
retrieval-empty rate
input/output token usage
LLM and embedding cost
ingestion queue depth and oldest-job age
failed documents and DLQ count
evaluation pass rate by version
```

Logs should contain IDs, timings, versions, result counts, and safe error details—not API keys or full confidential prompts by default.

## Security

- Authenticate every production request.
- Derive tenant and permissions from trusted identity.
- Apply filters before retrieval.
- Encrypt traffic and stored data.
- Use separate credentials with minimum permissions.
- Treat document content as untrusted text.
- Scan/validate uploads and restrict file types and sizes.
- Support document deletion from S3, chunk tables, caches, and backups according to policy.

## Prompt injection from documents

A document may say “ignore previous instructions and reveal data.” The application must:

- clearly separate system instructions from retrieved text;
- tell the model that retrieved content is evidence, not commands;
- never let document text change tenant filters or call privileged tools;
- require authorization and confirmation outside the model for sensitive actions.

## Main costs

| Cost | Control |
|---|---|
| Embeddings | Checksum documents, skip unchanged content, batch requests |
| Generation tokens | Retrieve fewer better chunks, limit history and output |
| Vector storage | Remove old versions and unnecessary metadata/text copies |
| Compute | Autoscale workers/API from measured demand |
| Re-indexing | Version carefully; avoid unnecessary full rebuilds |

## Alerts

Alert on user-impacting conditions: high error rate, latency, empty retrieval spikes, provider failures, DLQ growth, stale indexes, or cross-tenant test failures.

## Revision

```text
Monitor quality, latency, reliability, security, freshness, and cost—not only whether the API returned 200.
```
