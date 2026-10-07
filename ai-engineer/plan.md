# Generative AI Application Engineer Roadmap

## Goal

Become a good Generative AI application engineer who can build useful, reliable applications with existing foundation models.

You will learn to:

- call hosted and open-source language models;
- design prompts and validated structured outputs;
- build document ingestion and RAG pipelines;
- create controlled tool-calling workflows and agents;
- evaluate nondeterministic output;
- handle prompt injection, data access, and other security risks;
- expose AI features through FastAPI;
- manage latency, cost, rate limits, and production failures;
- explain your architecture clearly in interviews.

You do **not** need to become an ML researcher or train models from scratch.

## Do you need machine learning?

You do not need a full machine-learning curriculum for this goal.

Skip for now:

- linear and logistic regression;
- decision trees and random forests;
- training neural networks with PyTorch;
- backpropagation mathematics;
- extensive probability and calculus;
- computer-vision model training;
- distributed GPU training.

You still need a small amount of model intuition:

- tokens and context windows;
- embeddings and cosine similarity;
- what inference means;
- temperature and sampling;
- pretraining versus fine-tuning;
- why hallucinations happen;
- why AI output must be evaluated.

This is closer to learning how a database works well enough to design good backend systems. You do not need to implement the database engine.

## What a Generative AI engineer actually builds

```text
user or business problem
        ↓
application workflow
        ↓
prompt + context + tools
        ↓
foundation model
        ↓
validated output
        ↓
evaluation, monitoring, and iteration
```

The model API call is usually the easiest part. Most engineering effort goes into context, data permissions, output validation, tools, failure handling, evaluation, latency, and cost.

## Recommended stack

Use one small stack instead of learning every framework:

- Python
- FastAPI and Pydantic
- one hosted LLM provider through its official Python SDK
- PostgreSQL and pgvector, or one simple vector database
- Redis only when caching or short-lived state is actually needed
- Docker
- pytest for deterministic code
- a small custom evaluation runner for AI behavior
- Hugging Face Transformers only for basic open-model inference

Start with ordinary Python. Learn LangChain, LlamaIndex, or another orchestration framework only after you can implement the basic workflow yourself.

---

## Module 1 — Generative AI and LLM foundations

Goal: understand enough about language models to build applications and discuss tradeoffs.

Learn:

- generative AI versus traditional predictive ML;
- foundation model and large language model;
- tokenization and token IDs;
- prompt tokens and generated tokens;
- context window;
- transformer and attention intuition;
- inference;
- text generation one token at a time;
- temperature, top-p, and maximum output tokens;
- hallucination;
- pretrained model, instruction-tuned model, and reasoning model conceptually;
- hosted models versus self-hosted open models;
- latency, cost, privacy, and quality tradeoffs;
- model knowledge cutoff versus information supplied at request time.

You should be able to explain:

```text
text input
→ tokenizer creates token IDs
→ model processes tokens and context
→ model predicts likely next tokens
→ tokenizer converts output IDs back to text
```

Hands-on work:

- call one hosted model using its official SDK;
- run one small open model through a Hugging Face pipeline;
- compare outputs at different temperatures;
- inspect how a tokenizer splits several inputs;
- record input tokens, output tokens, latency, and estimated cost.

Interview topics:

- What is a token?
- What is a context window?
- Why can an LLM hallucinate?
- What does temperature control?
- Hosted versus self-hosted models?
- Why is a larger model not always the best production choice?

Do not study transformer mathematics deeply. Attention intuition is enough at this stage.

---

## Module 2 — Prompt engineering and structured output

Goal: make model behavior clearer, more reliable, and easier for software to consume.

Learn:

- clear task, context, constraints, and output contract;
- instruction hierarchy and message roles;
- zero-shot and few-shot prompting;
- delimiters around untrusted input;
- positive instructions and explicit refusal behavior;
- separating instructions from data;
- structured JSON output;
- schema validation with Pydantic;
- retries for invalid output;
- deterministic validation after generation;
- prompt templates and prompt versioning;
- why asking for hidden reasoning is not a reliability strategy.

Basic flow:

```text
validated application input
→ prompt builder
→ model call
→ structured result
→ Pydantic validation
→ business rules
→ API response
```

Project 1: structured support-ticket analyzer

Input:

```json
{
  "subject": "Cannot access my account",
  "description": "Password reset link has expired twice"
}
```

Validated output:

```json
{
  "category": "account_access",
  "priority": "high",
  "sentiment": "frustrated",
  "summary": "Customer cannot complete password reset",
  "recommended_action": "Verify identity and issue a fresh reset link"
}
```

Implement:

- FastAPI endpoint;
- prompt builder separated from the route;
- Pydantic output schema;
- one retry for malformed output;
- fallback error response;
- prompt version, model, latency, and token-usage logging.

Interview topics:

- Why structured output instead of parsing prose?
- How do few-shot examples help?
- How do you prevent user text from becoming an instruction?
- What happens when output fails schema validation?
- How do you version and compare prompts?

---

## Module 3 — Model API engineering

Goal: treat the model provider as an unreliable external dependency.

Learn:

- provider client wrapper;
- configuration and secret management;
- request timeout;
- retry with exponential backoff and jitter;
- rate-limit handling;
- which failures are safe to retry;
- idempotency for tool actions and jobs;
- streaming responses;
- cancellation when the client disconnects;
- concurrency limits;
- model fallback;
- token and cost budgets;
- caching and when cached AI output is unsafe;
- provider-specific code behind an application interface.

Suggested structure:

```text
app/
├── api/
├── models/
├── services/
│   └── ticket_analyzer.py
└── ai/
    ├── client.py
    ├── prompts.py
    └── schemas.py
```

Important boundary:

```python
class ModelClient:
    async def generate_structured(
        self,
        prompt: str,
        output_schema: type[BaseModel],
    ) -> BaseModel:
        ...
```

Application services depend on this boundary rather than spreading provider calls through route files.

Interview topics:

- Handling `429`, timeout, and provider outage;
- retryable versus non-retryable errors;
- streaming tradeoffs;
- limiting concurrency and cost;
- switching models without rewriting business logic;
- fallback behavior.

---

## Module 4 — Embeddings and semantic search

Goal: understand the retrieval foundation used by RAG.

Learn:

- embedding as a vector representation;
- semantic similarity;
- dot product and cosine similarity intuitively;
- embedding dimension;
- document embedding versus query embedding;
- nearest-neighbor search;
- vector index;
- top-k results;
- similarity threshold;
- metadata filters;
- semantic versus keyword search;
- hybrid retrieval;
- reranking;
- embedding-model versioning.

Only one small piece of math is required:

```text
cosine similarity asks whether two vectors point in a similar direction
```

Hands-on work:

- embed a collection of support articles;
- embed a user query;
- retrieve the closest articles;
- compare semantic and keyword results;
- add product and tenant metadata filters;
- inspect bad retrieval results.

Interview topics:

- What are embeddings?
- Why does cosine similarity work for semantic search?
- What does top-k mean?
- Why are metadata filters essential?
- When is hybrid search better?
- Why must an embedding model change trigger re-indexing?

---

## Module 5 — Document ingestion and RAG

Goal: build a complete retrieval-augmented generation pipeline.

Learn the ingestion path:

```text
document
→ extract text
→ clean and normalize
→ split into chunks
→ attach metadata
→ generate embeddings
→ store text + vector + metadata
```

Learn the query path:

```text
question
→ create query embedding
→ apply permission filters
→ retrieve candidates
→ optionally rerank
→ construct grounded prompt
→ generate answer
→ return answer with citations
```

Important topics:

- PDF, HTML, Markdown, and plain-text extraction;
- chunk size and overlap;
- heading-aware and semantic chunking conceptually;
- retaining source, page, section, tenant, and access metadata;
- incremental indexing;
- document update and deletion;
- duplicate chunks;
- retrieval context budget;
- context ordering;
- citations;
- “I do not know” behavior;
- retrieval failure versus generation failure;
- RAG does not guarantee truth.

Project 2: multi-tenant knowledge assistant

- Ingest Markdown and PDF documents through a background job.
- Store chunks and embeddings.
- Restrict retrieval by tenant and user access.
- Answer only from retrieved evidence.
- Return source title, section/page, and document ID.
- Refuse when evidence is insufficient.
- Support document replacement and deletion.
- Record retrieved chunks for later evaluation.

Interview topics:

- Explain a RAG pipeline end to end.
- How do you choose chunk size?
- RAG versus fine-tuning?
- How do you handle stale documents?
- How do you avoid cross-tenant leakage?
- What if retrieval returns irrelevant text?
- Why evaluate retrieval separately from the final answer?

---

## Module 6 — Tool calling, workflows, and agents

Goal: let a model interact with application capabilities safely.

Learn:

- tool name, purpose, and argument schema;
- model requests a tool; application executes it;
- validate tool arguments with Pydantic;
- return tool results as untrusted data;
- deterministic workflow versus agentic loop;
- workflow state;
- maximum step/tool-call limits;
- retries and idempotency;
- read tools versus write tools;
- least-privilege credentials;
- human approval before consequential actions;
- audit log;
- when not to use an agent.

Tool lifecycle:

```text
user request
→ model selects a tool and arguments
→ application validates permissions and arguments
→ application executes the tool
→ tool result returns to the model
→ model creates the final response
```

Project 3: approval-gated support copilot

Tools:

- `search_knowledge_base`;
- `get_order_status`;
- `draft_customer_email`;
- `send_customer_email` only after human approval.

Requirements:

- read-only tools may run automatically;
- email sending requires explicit approval;
- every tool argument is validated;
- every call has a timeout;
- repeated write calls use an idempotency key;
- maximum number of workflow steps;
- complete audit trail;
- retrieved documents and tool output cannot override system instructions.

Interview topics:

- Tool calling versus agents;
- workflow versus open-ended loop;
- preventing infinite loops;
- approval gates;
- idempotent write operations;
- prompt injection through tool output;
- why tools should have narrow permissions.

Do not start with multi-agent frameworks. A controlled single workflow is more useful and easier to reason about.

---

## Module 7 — Conversation state and memory

Goal: maintain useful context without sending unlimited chat history.

Learn:

- model APIs are usually stateless from your application's perspective;
- conversation and message persistence;
- recent-message window;
- summarizing older messages;
- semantic retrieval from conversation history;
- user profile versus conversation facts;
- short-term versus long-term memory;
- token-budget management;
- memory expiry and deletion;
- tenant/user isolation;
- never treating generated summaries as guaranteed facts;
- concurrent message updates.

Design options:

```text
recent messages
+ compact conversation summary
+ retrieved relevant memories
+ current user message
= model context
```

Project addition: add conversations to the support copilot without allowing one user's history to appear in another user's session.

Interview topics:

- What does “memory” mean in an LLM application?
- Why not send the full conversation forever?
- How do you summarize safely?
- How do you delete a user's remembered data?
- How do you prevent cross-session leakage?

---

## Module 8 — Evaluation and testing GenAI systems

Goal: prove whether the application works and detect regressions.

Learn:

- probabilistic output still needs deterministic engineering checks;
- representative evaluation dataset;
- golden examples;
- offline evaluation versus production monitoring;
- exact and schema-based checks;
- classification/extraction metrics;
- retrieval recall@k and mean reciprocal rank conceptually;
- answer correctness, groundedness, relevance, and completeness;
- citation correctness;
- tool-selection and tool-argument accuracy;
- human review;
- model-as-judge and its limitations;
- pairwise comparison;
- regression testing after model, prompt, or index changes;
- error taxonomy.

Evaluate the RAG layers separately:

```text
Did retrieval find the required evidence?
        ↓
Did the answer use that evidence correctly?
        ↓
Were citations and refusal behavior correct?
```

Build an evaluation record such as:

```json
{
  "question": "How long is the refund window?",
  "required_document_ids": ["refund-policy"],
  "expected_facts": ["30 days"],
  "should_refuse": false
}
```

Project work:

- create at least 50 representative cases;
- include normal, ambiguous, adversarial, and no-answer cases;
- run them after every important prompt/model/retrieval change;
- compare quality, latency, and cost;
- inspect failures rather than reporting only one score.

Interview topics:

- Why are a few manual examples insufficient?
- What is a golden dataset?
- How do you evaluate RAG?
- What are the risks of model-as-judge?
- How do you evaluate a tool-using workflow?
- What should block a production release?

---

## Module 9 — Security and responsible GenAI

Goal: recognize threats created by models, retrieved data, and tools.

Learn:

- direct and indirect prompt injection;
- untrusted documents and tool results;
- instruction/data separation;
- least privilege;
- allow-listed tools and parameters;
- human approval for external side effects;
- PII and secret redaction;
- data retention;
- provider privacy and training settings;
- tenant isolation in retrieval;
- output encoding when displaying generated HTML/Markdown;
- abuse limits;
- unsafe-content handling appropriate to the product;
- audit trails;
- why prompts alone are not security controls.

Security principle:

```text
The model may propose an action.
Application code decides whether the action is allowed.
```

Red-team your projects with:

- “ignore previous instructions” requests;
- malicious instructions inside an uploaded document;
- requests for another tenant's data;
- tool arguments containing unexpected fields;
- repeated write-tool calls;
- attempts to reveal secrets or system instructions.

Interview topics:

- Prompt injection versus jailbreak;
- securing RAG;
- securing tool calls;
- why output validation is not authorization;
- handling sensitive enterprise data;
- designing an approval boundary.

---

## Module 10 — Production GenAI systems

Goal: operate AI features reliably in real applications.

Learn:

- FastAPI and Pydantic boundaries;
- async I/O and blocking provider SDKs;
- background document-ingestion jobs;
- durable queues and workers conceptually;
- batching embedding requests;
- caching prompts, embeddings, and retrieval carefully;
- rate limits and concurrency control;
- timeout, retry, and fallback policies;
- health checks;
- logs, traces, and metrics;
- model, prompt, schema, embedding, and index versioning;
- canary rollout and rollback;
- feature flags;
- latency percentiles;
- cost per request and per successful task;
- token budgets;
- provider outage behavior;
- data deletion and re-indexing jobs.

Observe each stage:

```text
request validation time
retrieval time and document IDs
model latency and token usage
tool calls and durations
validation/retry count
final status and user feedback
```

Capstone: production-style enterprise support assistant

- FastAPI service;
- tenant-scoped ingestion API;
- durable chunking and embedding job;
- hybrid retrieval and citations;
- conversation state;
- structured model output;
- controlled read tools;
- one approval-gated write tool;
- evaluation command;
- prompt/model/index versions;
- cost, latency, retrieval, and tool tracing;
- Docker setup;
- clear architecture and threat-model documentation.

Interview topics:

- How do you reduce latency?
- How do you control cost?
- What do you cache?
- How do you roll out a new model safely?
- What happens during provider outage?
- How do you make document ingestion resumable?
- What do you monitor?

---

## Module 11 — Fine-tuning and open models: decision-level knowledge

Goal: know when these approaches are relevant without becoming a model-training specialist.

Learn conceptually:

- prompt engineering;
- RAG;
- supervised fine-tuning;
- parameter-efficient fine-tuning such as LoRA;
- quantization;
- local/open-model inference;
- model licenses;
- GPU memory constraints;
- serving throughput and batching.

Decision guide:

```text
Need current/private facts?        → RAG
Need consistent output format?     → schema + prompting first
Need a repeatable style/behavior?  → consider fine-tuning
Need tools or live system data?    → tool calling
Need strict deterministic logic?   → normal application code
```

You do not need to fine-tune a model for the first portfolio. Be able to explain the tradeoff and run a small open model locally if your hardware permits.

Interview topics:

- Fine-tuning versus RAG;
- what LoRA changes conceptually;
- quantization tradeoffs;
- hosted versus self-hosted inference;
- why a fine-tuned model still needs evaluation and application safeguards.

---

## Module 12 — Interview preparation and system design

Goal: explain your projects and design a GenAI system under interview constraints.

### Questions you must answer

LLM foundations:

- What are tokens, context windows, and embeddings?
- What is hallucination?
- How do temperature and token limits affect output?

Application design:

- How do you make model output reliable?
- How do tool calls work?
- Why keep provider code behind a wrapper?
- How do you handle timeouts, rate limits, and malformed output?

RAG:

- Explain ingestion and query flows.
- How do you choose chunks and top-k?
- How do you handle updates and deletions?
- How do you enforce permissions?
- How do you evaluate retrieval and generation separately?

Agents:

- Workflow versus agent?
- How do you limit steps and permissions?
- Where do you require human approval?
- How do you prevent duplicate write actions?

Production:

- How do you monitor quality, latency, and cost?
- How do you roll out prompt/model changes?
- What happens if the model provider is unavailable?
- How do you investigate a bad answer?

### GenAI system-design framework

For any design question, cover:

1. User and business goal.
2. Input and output contract.
3. Data sources and access control.
4. Simple non-AI or single-call baseline.
5. Prompt, retrieval, and tool workflow.
6. Storage and background jobs.
7. Evaluation dataset and success metrics.
8. Failure handling and fallback.
9. Security and privacy.
10. Latency, scale, and cost.
11. Monitoring, versioning, and rollback.

### Project explanation framework

```text
problem
→ constraints and users
→ first baseline
→ architecture
→ your contribution
→ hardest failure/tradeoff
→ evaluation method
→ production safeguards
→ measured result
→ next improvement
```

Never invent production metrics. If a project was not deployed, report offline evaluation honestly.

---

## Portfolio projects

Build three deep projects instead of many chatbot clones.

### Project 1 — Structured support-ticket analyzer

Shows prompting, schemas, Pydantic validation, API design, retries, and model telemetry.

### Project 2 — Multi-tenant RAG knowledge assistant

Shows ingestion, chunking, embeddings, vector search, access filters, citations, deletion, background jobs, and evaluation.

### Project 3 — Approval-gated support copilot

Shows tool calling, workflow state, conversation memory, read/write boundaries, idempotency, security, human approval, and observability.

Project 3 can extend Project 2 so the final portfolio tells one coherent story.

## Suggested 12-week sequence

This is a guide, not a deadline.

| Weeks | Focus | Deliverable |
|---|---|---|
| 1 | LLM foundations and provider SDK | model comparison notebook/script |
| 2 | Prompting and structured outputs | ticket analyzer |
| 3 | API reliability | retries, streaming, budgets, telemetry |
| 4 | Embeddings and vector search | semantic article search |
| 5–6 | Ingestion and RAG | tenant-safe knowledge assistant |
| 7 | RAG evaluation | retrieval and answer evaluation set |
| 8–9 | Tools and workflows | support copilot with approval |
| 10 | Memory and security | conversation state + threat cases |
| 11 | Productionization | jobs, Docker, monitoring, fallbacks |
| 12 | Interview preparation | architecture walkthrough and system design |

Weekly learning balance:

- 25% concepts;
- 60% implementation and debugging;
- 15% evaluation and explaining your decisions.

## Definition of interview-ready

You are ready when you can:

- explain tokens, context windows, embeddings, and hallucinations;
- build an LLM endpoint with validated structured output;
- handle timeouts, rate limits, malformed output, and provider failure;
- build an ingestion and RAG pipeline without hiding everything behind a framework;
- evaluate retrieval separately from answer generation;
- build a controlled tool workflow with approval for write operations;
- explain conversation memory and tenant isolation;
- identify prompt-injection risks;
- monitor latency, tokens, cost, retrieval, and tool calls;
- demonstrate two or three serious projects and defend your design decisions.

## Topics to postpone

- classical ML algorithms;
- training neural networks from scratch;
- deep PyTorch training knowledge;
- advanced mathematics;
- training foundation models;
- custom CUDA kernels;
- distributed GPU training;
- reinforcement learning;
- complex fine-tuning pipelines;
- fully autonomous and multi-agent systems;
- chasing every new framework;
- advanced Kubernetes.

## Learning rule

For every module:

1. Understand the problem and vocabulary.
2. Implement the smallest version with ordinary Python.
3. Create representative evaluation cases.
4. Inspect failures.
5. Add complexity only when a failure justifies it.
6. Explain the design without looking at notes.

## Primary references

- [OpenAI API quickstart](https://platform.openai.com/docs/quickstart)
- [OpenAI Evals API](https://platform.openai.com/docs/api-reference/evals)
- [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/index)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Docker getting started](https://docs.docker.com/get-started/)

Use official documentation for provider and library APIs. Framework tutorials can help with a first experiment, but the portfolio should demonstrate your own architecture, evaluation data, and engineering decisions.
