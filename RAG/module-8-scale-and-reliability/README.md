# Module 8 — Scale and reliability

Scale the component that is actually under pressure.

```text
More questions  -> add API instances; optimize retrieval and LLM concurrency
More documents  -> add ingestion workers; batch embeddings
Slower searches -> tune queries/indexes; then scale the vector store
Provider limits -> queue, throttle, retry and use fallback behavior
```

## Queue and worker behavior

Every ingestion job should be idempotent: retrying the same document/version must not create duplicate active chunks.

```text
Queue -> worker attempt -> success
                       -> temporary failure -> delayed retry
                       -> repeated failure -> dead-letter queue + alert
```

Use exponential backoff with jitter. Do not retry permanent errors such as an unsupported corrupt file forever.

## Batch work

Generate embeddings in supported batches to reduce network overhead and cost. Keep job payloads small—store files in S3 and put only IDs in the queue.

## Caching

Safe candidates:

- embeddings for repeated normalized questions;
- retrieval results keyed by tenant, permissions, index version, and query;
- public answers with short TTL when the underlying version is known.

Avoid broad answer caches for permission-sensitive data.

## Vector-store scaling path

```text
1. Exact pgvector search on small data
2. Add normal metadata indexes
3. Measure with EXPLAIN ANALYZE
4. Add HNSW/IVFFlat if needed
5. Increase database resources/read replicas where suitable
6. Partition/shard or select a dedicated vector store only from measured need
```

Approximate indexes trade some recall for speed. Always rerun retrieval evaluations after index changes.

## Zero-downtime re-indexing

Use an `index_version`:

```text
Build version 2 beside active version 1
-> evaluate version 2
-> atomically mark version 2 active
-> retain version 1 briefly for rollback
-> delete version 1 later
```

This is useful when changing embedding models because embeddings from different models should not be mixed in one search index.

## Failure behavior

- Vector store unavailable: return a clear temporary error, not an ungrounded answer.
- LLM unavailable: retry within a strict budget, then fail clearly.
- Ingestion delayed: continue serving the last valid index and show freshness internally.
- One bad document: isolate it; do not stop the entire batch.

## Revision

```text
Scale API and ingestion independently, make jobs repeatable, and version every index-changing operation.
```
