# Resume RAG — Deployable Free-Tier Project

Upload multiple PDF, DOCX, or TXT resumes and ask questions across selected resumes.

```text
Which candidates have FastAPI experience?
Compare the selected candidates' backend skills.
Who has worked with MongoDB and Redis?
```

## Stack

```text
React, compiled and served by FastAPI
FastAPI on Render Free
Cloudinary Free for authenticated original files
Neon Free PostgreSQL + pgvector for metadata, chunks and vectors
Gemini API Free Tier for embeddings and answers
```

The deployed app is stateless. It does not depend on Render's temporary filesystem.

## Read first

1. [Architecture](ARCHITECTURE.md)
2. [Local development](LOCAL-DEVELOPMENT.md)
3. [Deploy today](DEPLOYMENT.md)

## Run locally with cloud services

Create `.env` from the example and fill in your credentials:

```bash
cp .env.example .env
cd frontend && npm install && npm run build && cd ..
uv sync
uv run uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000). It redirects to the React app at `/app/`. All backend routes, including API documentation at `/api/docs`, live below `/api`.

Local development and the deployed application use the same Cloudinary, Neon, and Gemini interfaces. Use separate development and production resources if the project will hold real resumes.

## Supported files

- PDF with selectable text
- DOCX
- UTF-8 TXT

Scanned PDFs require OCR and are rejected clearly in this version.

## Tests

```bash
uv run pytest
```

Unit tests do not call cloud services.
