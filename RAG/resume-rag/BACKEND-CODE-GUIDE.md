# Backend code guide

This guide explains the backend of the Resume RAG project in simple terms.

## 1. What the backend does

The backend has four main jobs:

1. Accept resume files from the React application.
2. Extract and split their text, create embeddings, and save everything.
3. Find the resume sections most related to a user's question.
4. Ask Gemini to answer using those sections and stream the answer to React.

```text
React
  -> FastAPI
      -> Cloudinary: original resume files
      -> Neon PostgreSQL: resume details, text chunks, vectors
      -> Gemini: embeddings and generated answers
```

The backend code is inside `app/`.

```text
app/
├── main.py             Routes and application startup
├── config.py           Environment variables and settings
├── models.py           API request and response shapes
├── database.py         Database tables, engine, and sessions
├── parsers.py          PDF, DOCX, and TXT text extraction
├── text_processing.py  Text cleanup and chunking
├── ai_client.py        Gemini embeddings and answer generation
├── cloud_storage.py    Cloudinary upload and deletion
└── retrieval.py        Vector similarity search
```

## 2. Complete upload flow

When the user uploads a resume:

```text
1. React sends multipart/form-data to POST /api/resumes.
2. FastAPI checks the file extension and size.
3. parsers.py extracts text from the file held in memory.
4. text_processing.py cleans the text.
5. text_processing.py splits it into overlapping chunks.
6. ai_client.py asks Gemini to create one vector per chunk.
7. cloud_storage.py stores the original file in Cloudinary.
8. database.py stores resume metadata, chunks, and vectors in Neon.
9. FastAPI returns information about the uploaded resume.
```

The file is never permanently written to the FastAPI server's disk.

## 3. Complete question flow

```text
1. React sends a question and selected resume IDs.
2. Gemini converts the question into a 768-number query vector.
3. PostgreSQL compares that vector with stored chunk vectors.
4. The three closest chunks are returned.
5. retrieval.py turns those chunks into labelled context.
6. Gemini receives the question plus context.
7. Gemini streams small pieces of the answer.
8. FastAPI forwards each piece to React immediately.
9. React gradually renders the answer as Markdown.
```

This is RAG: retrieve relevant data first, then generate an answer from it.

---

# 4. `config.py`

This file provides one place for application configuration.

## `PROJECT_DIR`

```python
PROJECT_DIR = Path(__file__).resolve().parent.parent
```

It resolves the project directory regardless of the terminal's current directory. It is used to locate `.env` and the compiled React application.

## `Settings`

`Settings` extends Pydantic's `BaseSettings`. Pydantic reads environment variables, converts their types, and validates configured limits.

| Python field | Environment variable | Purpose |
|---|---|---|
| `database_url` | `DATABASE_URL` | Neon PostgreSQL connection |
| `cloudinary_url` | `CLOUDINARY_URL` | Cloudinary account credentials |
| `gemini_api_key` | `GEMINI_API_KEY` | Authenticates Gemini calls |
| `gemini_embedding_model` | `GEMINI_EMBEDDING_MODEL` | Model that creates vectors |
| `gemini_chat_model` | `GEMINI_CHAT_MODEL` | Model that writes answers |
| `max_upload_mb` | `MAX_UPLOAD_MB` | Maximum size of one uploaded file |
| `top_k` | `TOP_K` | Number of relevant chunks retrieved; currently 3 |

`SettingsConfigDict` tells Pydantic to load `.env`, read it as UTF-8, and ignore unrelated environment variables.

## `async_database_url`

Neon provides a normal PostgreSQL URL. SQLAlchemy is using the asynchronous `asyncpg` driver, so this property:

- changes `postgresql://` to `postgresql+asyncpg://`;
- changes the SSL parameter into the form accepted by `asyncpg`;
- removes the unsupported `channel_binding` option.

It returns a database URL suitable for `create_async_engine()`.

## `validate_runtime()`

This checks that the three essential secrets exist. The application refuses to start when any are missing, instead of failing later during a user request.

## `get_settings()` and `settings`

`@lru_cache` creates the settings only once. Every backend file imports the same settings object instead of repeatedly reading `.env`.

---

# 5. `models.py`

These are Pydantic API models. They validate incoming JSON and control outgoing JSON.

## `ResumeSummary`

Represents a resume shown in the UI.

```json
{
  "resume_id": "7f...",
  "original_name": "candidate.pdf",
  "uploaded_at": "2026-10-14T12:30:00Z",
  "chunk_count": 6
}
```

## `UploadResponse`

Returned after uploading one or more files:

```json
{
  "resumes": [
    {
      "resume_id": "7f...",
      "original_name": "candidate.pdf",
      "uploaded_at": "2026-10-14T12:30:00Z",
      "chunk_count": 6
    }
  ]
}
```

## `QuestionRequest`

Expected request body for asking a question:

```json
{
  "question": "Does this candidate know FastAPI?",
  "resume_ids": ["7f..."],
  "top_k": 3
}
```

Validation rules:

- question: 2–1,000 characters;
- resume IDs: 1–50 IDs;
- optional `top_k`: 1–15.

If `top_k` is absent, the configured value of 3 is used.

## `RetrievedSource`

Represents one chunk returned by vector search.

```json
{
  "resume_id": "7f...",
  "resume_name": "candidate.pdf",
  "chunk_number": 2,
  "score": 0.8124,
  "text": "Worked with Python and FastAPI..."
}
```

The score is similarity, where a larger value means the chunk is more related to the question.

## `QuestionResponse`

Used by the non-streaming question endpoint:

```json
{
  "answer": "The candidate has FastAPI experience.",
  "sources": []
}
```

---

# 6. `database.py`

This file defines the PostgreSQL tables and database connection objects.

## `EMBEDDING_DIMENSIONS`

Every embedding must contain exactly 768 floating-point numbers. The document vectors and question vectors must use the same size.

## `Base`

All SQLAlchemy table classes inherit from this base. `AsyncAttrs` enables asynchronous SQLAlchemy behaviour.

## `ResumeRecord`

Maps to the `resumes` table.

| Column | Meaning |
|---|---|
| `id` | Application-generated UUID |
| `original_name` | Filename shown to the user |
| `cloudinary_public_id` | Cloudinary identifier used for deletion |
| `file_url` | Cloudinary secure URL |
| `uploaded_at` | Upload date and time |
| `chunk_count` | Number of searchable text chunks |
| `embedding_model` | Model used to create its vectors |

`chunks` is the relationship to `ResumeChunk`. `cascade="all, delete-orphan"` means deleting a resume record also deletes its associated chunk objects.

## `ResumeChunk`

Maps to the `resume_chunks` table.

| Column | Meaning |
|---|---|
| `id` | Auto-incrementing chunk ID |
| `resume_id` | Foreign key pointing to `resumes.id` |
| `chunk_number` | Position of the chunk in the resume |
| `text` | Original searchable text |
| `embedding` | 768-dimensional pgvector value |

`ondelete="CASCADE"` asks PostgreSQL to delete chunks when their parent resume is deleted. The `resume_id` index helps queries filtered by resume.

## `engine`

The async SQLAlchemy engine owns the database connection pool. `pool_pre_ping=True` checks pooled connections before reuse, which helps when Neon has closed an idle connection.

## `SessionFactory`

Creates short-lived database sessions. A session is the unit used to run queries, add records, commit, or roll back.

`expire_on_commit=False` keeps loaded object values available after committing.

## `initialize_database()`

At startup it:

1. enables PostgreSQL's `vector` extension;
2. creates missing tables based on the SQLAlchemy models.

For a larger production project, schema changes should normally use migrations such as Alembic instead of `create_all()`.

---

# 7. `parsers.py`

This file extracts text from the in-memory file bytes.

## `SUPPORTED_EXTENSIONS`

Only `.pdf`, `.docx`, and `.txt` are accepted.

## `extract_text(filename, content)`

Input:

- `filename`: used to identify the extension;
- `content`: the uploaded file as bytes.

Processing:

- PDF: `pypdf.PdfReader` extracts text page by page.
- DOCX: `python-docx` reads each paragraph.
- TXT: Python decodes the bytes as UTF-8.
- The extracted value is passed to `normalize_text()`.

Response: one cleaned Python string.

It raises `ValueError` for unsupported files, invalid TXT encoding, and files without readable text. Image-only scanned PDFs have no embedded text, so they require OCR and are rejected in this version.

---

# 8. `text_processing.py`

## `normalize_text(text)`

This removes null characters, repeated spaces, tabs, and noisy line breaks while preserving paragraph boundaries.

Input:

```text
Python     Developer

Worked with FastAPI.
```

Output:

```text
Python Developer

Worked with FastAPI.
```

## `chunk_text(text, chunk_size_words=180, overlap_words=30)`

Large documents are split because retrieval should search focused sections rather than one complete resume.

- Each chunk contains at most 180 words.
- Consecutive chunks share 30 words.
- The overlap prevents information at a chunk boundary from losing its surrounding context.

Example:

```text
Chunk 1: words 0–179
Chunk 2: words 150–329
Chunk 3: words 300–479
```

Response: `list[str]` containing the chunks.

The function validates that chunk size is positive and overlap is smaller than chunk size.

---

# 9. `cloud_storage.py`

## `parse_cloudinary_url(value)`

Parses this format:

```text
cloudinary://api_key:api_secret@cloud_name
```

Response:

```python
{
    "cloud_name": "...",
    "api_key": "...",
    "api_secret": "...",
}
```

`unquote()` supports URL-encoded characters inside credentials.

## `configure_cloudinary()`

Passes the parsed fields to the Cloudinary SDK. `secure=True` makes returned asset URLs use HTTPS.

It runs once when this module is imported.

## `upload_resume(resume_id, extension, content)`

The Cloudinary SDK is synchronous. Calling it directly inside an async FastAPI route would block that process. `asyncio.to_thread()` runs the blocking upload in a worker thread.

Important upload settings:

- `resource_type="raw"`: keeps PDF/DOCX/TXT as normal files;
- `type="authenticated"`: the asset is not a normal public Cloudinary asset;
- `public_id`: gives the file an organized unique path;
- `overwrite=False`: prevents accidental replacement.

Response:

```python
(public_id, secure_url)
```

## `delete_resume_asset(public_id)`

Deletes the authenticated raw asset. Both `ok` and `not found` are accepted so repeated cleanup is safe.

---

# 10. `ai_client.py`

This file communicates with the Gemini REST API through HTTP.

## `AIProviderError`

A custom exception used for safe messages. Routes convert it into an HTTP 503 response without exposing credentials or internal details.

## Shared HTTP client

### `start_ai_client()`

Creates one `httpx.AsyncClient` with:

- a 15-second connection timeout;
- a 120-second total operation timeout;
- up to 20 connections;
- up to 10 reusable keep-alive connections.

Reusing this client avoids creating a new TCP/TLS connection for every Gemini call, which improves latency.

### `close_ai_client()`

Closes the HTTP pool when FastAPI shuts down.

### `_client()`

Returns the shared client. It also creates it lazily if needed in a script or test outside FastAPI startup.

## `_gemini_error(response, action)`

Maps provider errors into understandable messages:

| Gemini status | Application meaning |
|---|---|
| 400 | Gemini rejected the request format |
| 401/403 | Invalid key or missing permission |
| 404 | Model unavailable |
| 429 | Quota/rate limit reached |
| 5xx | Gemini temporarily unavailable |

## `create_embeddings(texts, task_type)`

It sends multiple texts to Gemini's batch embedding endpoint.

`task_type` is important:

- `RETRIEVAL_DOCUMENT`: used while indexing resume chunks;
- `RETRIEVAL_QUERY`: used for a user's question.

Gemini can optimize vectors differently for stored documents and search queries while keeping them comparable.

Response:

```python
[
    [0.012, -0.081, ... 768 values],
    [0.025, 0.104, ... 768 values],
]
```

The function verifies that Gemini returns one 768-dimensional vector for every input string.

## `generate_answer(question, context)`

This is the older non-streaming answer method used by `POST /api/questions`.

It sends:

- a system instruction preventing invented resume facts;
- retrieved context;
- the user's question;
- low thinking level;
- maximum 800 output tokens.

It retries connection and Gemini 5xx failures up to three times. It removes internal thought parts and returns the final answer as one string.

## `stream_answer(question, context)`

This is used by the React UI.

It calls Gemini's `streamGenerateContent` endpoint with Server-Sent Event output. Gemini sends several `data:` lines instead of one final JSON response.

The function:

1. reads incoming lines asynchronously;
2. ignores non-data lines;
3. parses each JSON event;
4. ignores internal thought blocks;
5. yields visible text pieces.

Its return type is `AsyncIterator[str]`: callers use `async for` and receive text over time.

Although Gemini uses SSE upstream, the application converts the browser response into NDJSON so sources, tokens, completion, and errors can use explicit event types.

---

# 11. `retrieval.py`

## `retrieve(question_embedding, resume_ids, top_k)`

This performs vector similarity search.

Steps:

1. Remove duplicate IDs while preserving order using `dict.fromkeys()`.
2. Convert strings into UUID objects.
3. Calculate cosine distance between stored vectors and the question vector.
4. Filter results to only user-selected resumes.
5. Order from smallest distance to largest distance.
6. Return only the top three by default.

The score returned to the UI is:

```text
similarity = 1 - cosine distance
```

The response is a list of `RetrievedSource` models.

## `build_context(sources)`

Turns retrieved objects into text Gemini can understand:

```text
[Resume: candidate-a.pdf; chunk 2]
Worked with Python and FastAPI...

[Resume: candidate-b.pdf; chunk 4]
Developed Node.js microservices...
```

The labels help Gemini attribute information to the correct resume.

---

# 12. `main.py`

This is the application entry point and HTTP layer.

## `lifespan()`

Runs once around the lifetime of the FastAPI process.

At startup:

1. validate environment variables;
2. create the shared Gemini HTTP client;
3. enable pgvector and create missing database tables.

At shutdown:

1. close Gemini HTTP connections;
2. close the database engine.

## FastAPI configuration

```text
Swagger docs: /api/docs
ReDoc:        /api/redoc
OpenAPI JSON: /api/openapi.json
React files:  /app/
```

The static mount stays after API routes so it cannot take control of API paths.

## `GET /`

Redirects the browser to `/app/` with HTTP 307.

## `GET /api/health`

Returns:

```json
{"status": "ok"}
```

This only proves the FastAPI process is responding. It does not test Neon, Gemini, or Cloudinary.

## `GET /api/resumes`

Queries all resume records, newest first.

Response: HTTP 200 with a JSON array of `ResumeSummary` objects.

## `POST /api/resumes`

Request format: `multipart/form-data` with one or more fields named `files`.

Important steps:

1. reject missing files;
2. check the extension;
3. read no more than the allowed bytes plus one;
4. reject empty and oversized files;
5. extract and chunk text;
6. create embeddings;
7. upload the original to Cloudinary;
8. build one `ResumeRecord` and its `ResumeChunk` children;
9. commit them in a database transaction;
10. return uploaded resume summaries.

`zip(chunks, embeddings, strict=True)` guarantees every chunk has a matching embedding. `enumerate(..., start=1)` assigns human-readable chunk numbers.

If Cloudinary succeeds but the database commit fails, the code deletes the Cloudinary asset. This compensation prevents an unused file from being left behind.

Response: HTTP 201 with `UploadResponse`.

Common errors:

- 400: invalid type, empty file, unreadable text;
- 413: file too large;
- 503: Gemini unavailable or over quota.

## `DELETE /api/resumes/{resume_id}`

Steps:

1. validate the URL value as a UUID;
2. load the resume;
3. return 404 if it does not exist;
4. delete the original Cloudinary file;
5. delete the database record;
6. let cascade deletion remove its chunks;
7. commit.

Response: HTTP 204 with no response body.

## `POST /api/questions`

This is the non-streaming alternative.

It embeds the question, retrieves chunks, waits for Gemini's complete answer, and returns a normal `QuestionResponse` JSON object.

## `POST /api/questions/stream`

This is the endpoint used by React.

Before streaming begins, it:

1. validates `QuestionRequest` automatically through FastAPI/Pydantic;
2. creates the query embedding;
3. retrieves the top three chunks.

It returns `application/x-ndjson`. Every line is a separate JSON event.

First event:

```json
{"type":"sources","sources":[...]}
```

Text events while Gemini generates:

```json
{"type":"token","text":"The candidate "}
{"type":"token","text":"has FastAPI experience."}
```

Final event:

```json
{"type":"done"}
```

Streaming failure after HTTP streaming has started:

```json
{"type":"error","detail":"Gemini is temporarily unavailable."}
```

`Cache-Control: no-cache` prevents caching. `X-Accel-Buffering: no` asks compatible reverse proxies not to hold chunks before forwarding them.

---

# 13. Packages used

## Production packages

| Package | Why it is used |
|---|---|
| `fastapi[standard]` | Routes, validation integration, uploads, streaming responses, Uvicorn tooling |
| `pydantic-settings` | Typed `.env` and environment configuration |
| `sqlalchemy[asyncio]` | Async ORM models, queries, sessions, transactions, connection pool |
| `asyncpg` | Async PostgreSQL driver used below SQLAlchemy |
| `pgvector` | PostgreSQL vector column and cosine-distance SQL operations |
| `httpx` | Async HTTP calls and connection pooling for Gemini |
| `cloudinary` | Upload and delete original resume files |
| `pypdf` | Extract text from text-based PDF documents |
| `python-docx` | Extract paragraphs from DOCX files |

`fastapi[standard]` also brings common FastAPI runtime tools such as Uvicorn and multipart form handling.

## Development package

| Package | Why it is used |
|---|---|
| `pytest` | Runs unit tests for parsing, chunking, configuration helpers, and error handling |

## Python standard-library modules

The project also uses built-in modules such as:

- `asyncio`: threads for blocking Cloudinary calls and retry delays;
- `json`: Gemini events and NDJSON response lines;
- `pathlib`: safe filesystem paths and extensions;
- `uuid`: resume identifiers and validation;
- `datetime`: UTC upload timestamps;
- `io.BytesIO`: treat in-memory bytes like a file;
- `re`: text whitespace cleanup;
- `urllib.parse`: parse Cloudinary credentials.

---

# 14. Where data is stored

```text
Cloudinary
└── Original PDF/DOCX/TXT bytes

Neon PostgreSQL
├── resumes
│   └── Metadata and Cloudinary identifiers
└── resume_chunks
    └── Chunk text and 768-dimensional embeddings

FastAPI container
└── No permanent resume data
```

Gemini receives resume text to create embeddings and answers, but this application does not use Gemini as permanent storage.

---

# 15. Important design decisions

## Why async code?

Database and external HTTP calls spend time waiting. `async` allows FastAPI to work on other requests during that waiting time.

## Why store text and vectors together?

PostgreSQL can find the closest vectors and return their associated text in one query. A separate vector database is unnecessary for this small project.

## Why keep original files in Cloudinary?

Render's local filesystem is temporary. Cloudinary keeps the original files when the application container restarts.

## Why stream NDJSON?

The client must send a JSON POST body containing a question and resume IDs. NDJSON works naturally with a streamed POST response and supports different event types.

## Why retrieve only three chunks?

It reduces database output, Gemini input tokens, cost, and latency. It also reduces unrelated context. If answers regularly miss information, increase `TOP_K` after measuring retrieval quality.

## What is not implemented yet?

- authentication and per-user resume ownership;
- OCR for scanned PDFs;
- malware scanning;
- background job processing for large uploads;
- database migrations;
- chat-history persistence;
- request rate limiting;
- a vector index for very large datasets.

These are appropriate next steps before accepting real public users.
