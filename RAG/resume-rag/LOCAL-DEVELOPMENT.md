# Local development

Local development builds React as static files and runs FastAPI on your computer while using free development resources in Cloudinary, Neon, and Gemini.

```text
Local browser -> FastAPI -> compiled React files at /app/
                         -> API routes at /api/*
                             -> Cloudinary development folder
                             -> Neon development database
                             -> Gemini free API
```

## 1. Create the free services

### Cloudinary

Create a free account and copy the `CLOUDINARY_URL` from the dashboard.

The backend uploads files as authenticated raw assets. Never place the Cloudinary API secret in frontend JavaScript.

### Neon

Create a free PostgreSQL project and copy its connection string. Keep `sslmode=require`.

The application automatically runs:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

It also creates the `resumes` and `resume_chunks` tables on startup.

### Gemini

Create a free API key in Google AI Studio. The free tier is intended for learning and small projects and has rate limits.

## 2. Configure environment variables

```bash
cp .env.example .env
```

Update:

```text
DATABASE_URL
CLOUDINARY_URL
GEMINI_API_KEY
```

Never commit `.env`.

## 3. Start the project

```bash
cd frontend
npm install
npm run build
cd ..

uv sync
uv run uvicorn app.main:app --reload
```

Open `http://localhost:8000`. The root redirects to `/app/`. API docs are at `http://localhost:8000/api/docs`.

Run `npm run build` again after changing React code. The Docker deployment does this automatically.

## 4. Understand one upload

1. FastAPI reads the uploaded file into memory with a size limit.
2. PDF/DOCX/TXT parsing happens locally.
3. The text becomes overlapping chunks.
4. Gemini embeds the chunks.
5. Cloudinary stores the original privately.
6. One Neon transaction stores metadata, chunks, and vectors.

No resume is written permanently to the application filesystem.

## 5. Debugging order

```text
Upload rejected      -> file type, size, scanned PDF
Cloudinary failure   -> CLOUDINARY_URL and free-plan limits
Database failure     -> Neon URL, SSL and pgvector extension
Embedding failure    -> Gemini key/rate limit/model name
Bad search           -> inspect returned source chunks
Bad answer           -> verify sources first, then prompt/model
```

## 6. Separate development from production

For a portfolio demo, one set of free resources is acceptable. For real resumes, create separate resources, add login/ownership checks, and review each provider's privacy terms.
