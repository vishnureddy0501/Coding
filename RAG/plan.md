# RAG — Development and Architecture Plan

## Goal

Learn how to design, develop, test, deploy, and scale a real RAG application without getting buried in theory or code.

We will learn one module at a time using a practical example:

> A chatbot that answers questions from customer-success documents and Action Items Library information.

## What is RAG in one line?

```text
Find relevant information first -> give it to the LLM -> generate an answer
```

The LLM does not need to memorize our private data. The application retrieves the required data when the user asks a question.

## Complete learning path

### Module 1 — Understand the complete RAG flow

[Open Module 1](module-1-rag-flow/README.md)

- The problem RAG solves
- RAG versus normal LLM chat
- Documents, chunks, embeddings, vector search, and generation
- One complete question flow
- What RAG can and cannot do

**Outcome:** Explain how a RAG request works from user question to final answer.

### Module 2 — Data ingestion architecture

[Open Module 2](module-2-ingestion/README.md)

- Where documents come from
- Loading PDF, Markdown, web, and database content
- Cleaning and normalizing data
- Splitting documents into useful chunks
- Adding metadata such as tenant, source, feature, and permissions
- Creating embeddings and storing them
- New documents, updated documents, and deleted documents

**Outcome:** Design a reliable pipeline that keeps searchable knowledge current.

### Module 3 — Retrieval architecture

[Open Module 3](module-3-retrieval/README.md)

- Turning a question into an embedding
- Vector search in simple terms
- Keyword search versus vector search
- Hybrid search
- Metadata filtering and tenant isolation
- Reranking results
- Choosing how many chunks to retrieve

**Outcome:** Retrieve useful context instead of merely similar-looking text.

### Module 4 — Answer generation

[Open Module 4](module-4-generation/README.md)

- Building the final prompt
- Giving retrieved context to the LLM
- Asking the model to cite sources
- Handling “I could not find the answer”
- Preventing the model from inventing information
- Conversation history versus retrieved knowledge

**Outcome:** Generate answers grounded in retrieved data.

### Module 5 — Build the local development version

[Open Module 5](module-5-local-development/README.md)

```text
Local documents
    -> ingestion script
    -> local vector database
    -> FastAPI RAG endpoint
    -> LLM API
    -> simple chat UI
```

- Recommended local technology choices
- Local project structure
- Running ingestion manually
- Testing retrieval separately from answer generation
- Debugging bad answers
- Keeping secrets in `.env`

**Outcome:** Understand how all local development components fit together.

### Module 6 — Evaluation and testing

[Open Module 6](module-6-evaluation/README.md)

- Why a good-looking answer is not enough
- Creating a small question-and-answer test set
- Measuring retrieval quality
- Measuring answer correctness and faithfulness
- Testing tenant and permission filters
- Regression testing after changing chunking, prompts, or models
- Human review

**Outcome:** Know whether the RAG system is actually improving.

### Module 7 — Production architecture

[Open Module 7](module-7-production/README.md)

```text
Sources -> ingestion workers -> vector store
                                  ↑
User -> API -> retrieval service -> LLM -> answer
```

- Separating offline ingestion from online questions
- API, worker, queue, object storage, vector store, and LLM provider
- Docker-based deployment
- Development, staging, and production environments
- Background ingestion and scheduled synchronization
- Authentication, authorization, and tenant isolation
- Configuration and secret management

**Outcome:** Design a production system without mixing ingestion work with user requests.

### Module 8 — Scale and reliability

[Open Module 8](module-8-scale-and-reliability/README.md)

- What becomes slow as data and traffic grow
- Scaling API instances and ingestion workers separately
- Queues, retries, and dead-letter handling
- Batch embedding generation
- Caching frequent questions and retrieval results
- Vector database indexing
- Rate limits and LLM-provider failures
- Timeouts, fallbacks, and graceful degradation
- Zero-downtime document re-indexing

**Outcome:** Understand how the system continues working with more users and documents.

### Module 9 — Monitoring, security, and cost

[Open Module 9](module-9-operations/README.md)

- Logs, metrics, and traces for one RAG request
- Monitoring retrieval time, LLM time, errors, and token usage
- Tracking bad or unanswered questions
- Prompt injection from documents
- Protecting private customer data
- Data retention and deletion
- Main cost areas and practical cost controls

**Outcome:** Operate RAG safely and understand where money and failures go.

### Module 10 — RAG with the customer-success system

[Open Module 10](module-10-customer-success/README.md)

- What belongs in RAG
- What should remain a normal MongoDB/MCP tool call
- Combining RAG with MCP tools
- Searching documentation versus fetching current records
- Suggested architecture for an internal customer-success assistant

Example:

```text
"How does Action Items Library work?"
    -> RAG searches documentation

"Show current HIGH-priority templates"
    -> MCP tool queries MongoDB

"Explain the current templates using product documentation"
    -> MCP + RAG together
```

**Outcome:** Choose the correct approach instead of forcing every question through RAG.

## Technologies we will consider

We will choose the smallest suitable stack rather than installing everything.

| Need | Starting choice |
|---|---|
| API | FastAPI |
| Main application data | MongoDB |
| Local vector search | PostgreSQL + pgvector or a simple local vector store |
| Production vector search | pgvector first; dedicated vector database only if needed |
| Background work | Celery + Redis or the queue already used by the company |
| Raw documents | Local folder in development, S3 in production |
| LLM and embeddings | Provider APIs behind a small application interface |
| Monitoring | Existing logging/APM stack; Splunk if already used |
| Deployment | Docker, then the existing AWS deployment platform |

We will not begin with Kubernetes, Kafka, multiple agents, or a dedicated vector database unless scale proves they are necessary.

## How each module will be taught

Every module will contain:

1. A simple explanation
2. One architecture diagram
3. A real request flow
4. Local-development decisions
5. Production decisions
6. Common mistakes
7. A short revision summary

Code will be included only when it helps explain an architectural decision.

## Final project

[Open the Resume RAG project](resume-rag/README.md)

Design a **Customer Success Knowledge Assistant** that:

- answers product and feature questions from approved documents;
- cites the documents used;
- keeps tenant data isolated;
- uses MCP for current MongoDB records;
- uses RAG for unstructured documentation;
- works locally and has a clear production deployment design;
- can scale ingestion and question traffic independently.

## Learning rule

Complete one module before adding another technology. A reliable small RAG system is more valuable than a complicated system whose answers cannot be trusted.
