# Deploy today using free tiers

## Services

```text
Cloudinary -> file storage
Neon       -> PostgreSQL + pgvector
Gemini     -> embeddings + answer generation
Render     -> one container for React static files + FastAPI
```

## 1. Prepare accounts

1. Create Cloudinary Free and copy `CLOUDINARY_URL`.
2. Create Neon Free and copy `DATABASE_URL`.
3. Create a Gemini API key in Google AI Studio.
4. Push this repository to GitHub.

Do not commit any secret.

## 2. Test locally first

Create `.env`, start the API, upload two sample resumes, ask a question, and delete one resume. This verifies all three external integrations before deployment.

## 3. Deploy on Render

The included `render.yaml` and `Dockerfile` describe the service. Docker first builds React with Vite, then copies the compiled files into the FastAPI image. There is no separate frontend service.

In Render:

1. Create a new Blueprint/Web Service from the GitHub repository.
2. Set the root directory to `RAG/resume-rag` if deploying from the Coding repository.
3. Choose the Free plan.
4. Add secret environment variables:

```text
DATABASE_URL
CLOUDINARY_URL
GEMINI_API_KEY
```

5. Deploy and open the generated `onrender.com` URL.

The `/api/health` endpoint is used as the Render health check. Visiting `/` redirects to the React app at `/app/`; all backend endpoints are under `/api`.

## Free-tier realities

- Render sleeps after 15 minutes without traffic; the first request may take about a minute.
- Render's filesystem is temporary, which is why this app stores nothing there.
- Cloudinary Free uses monthly shared credits and limits raw files to 10 MB; this app defaults to 5 MB.
- Neon Free is suitable for a portfolio/demo and can scale to zero.
- Gemini Free has rate limits, and free-tier content may be used to improve Google products according to its terms.
- Ollama Cloud Free includes limited starter usage, not unlimited hosted compute.

This can cost ₹0 for a portfolio demo while you stay inside every provider's current limits. Free plans can change, so set usage alerts where available.

## Before accepting real public uploads

- Add user authentication and resume ownership.
- Scan uploads for malware.
- Add per-user and IP rate limits.
- Add a privacy notice and deletion policy.
- Do not expose Cloudinary credentials or raw authenticated URLs.
- Move to paid service tiers if uptime or privacy guarantees matter.
