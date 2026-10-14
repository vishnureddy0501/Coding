from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
import json
from uuid import UUID, uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import select

from app.ai_client import (
    AIProviderError,
    close_ai_client,
    create_embeddings,
    generate_answer,
    start_ai_client,
    stream_answer,
)
from app.cloud_storage import delete_resume_asset, upload_resume
from app.config import PROJECT_DIR, settings
from app.database import ResumeChunk, ResumeRecord, SessionFactory, engine, initialize_database
from app.models import QuestionRequest, QuestionResponse, ResumeSummary, UploadResponse
from app.parsers import SUPPORTED_EXTENSIONS, extract_text
from app.retrieval import build_context, retrieve
from app.text_processing import chunk_text


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Validate cloud configuration and prepare the Neon pgvector schema."""
    settings.validate_runtime()
    await start_ai_client()
    await initialize_database()
    try:
        yield
    finally:
        await close_ai_client()
        await engine.dispose()


app = FastAPI(
    title="Resume RAG",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.get("/", include_in_schema=False)
async def home() -> RedirectResponse:
    """Send the root URL to the React application."""
    return RedirectResponse(url="/app/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/resumes", response_model=list[ResumeSummary])
async def get_resumes() -> list[ResumeSummary]:
    async with SessionFactory() as session:
        records = (
            await session.scalars(select(ResumeRecord).order_by(ResumeRecord.uploaded_at.desc()))
        ).all()
    return [
        ResumeSummary(
            resume_id=str(item.id),
            original_name=item.original_name,
            uploaded_at=item.uploaded_at,
            chunk_count=item.chunk_count,
        )
        for item in records
    ]


@app.post(
    "/api/resumes",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resumes(files: list[UploadFile] = File(...)) -> UploadResponse:
    """Parse resumes, store originals in Cloudinary, and index them in Neon."""
    if not files:
        raise HTTPException(status_code=400, detail="Select at least one resume")

    saved: list[ResumeSummary] = []
    max_bytes = settings.max_upload_mb * 1024 * 1024

    for upload in files:
        filename = upload.filename or "resume"
        extension = Path(filename).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"{filename}: supported file types are PDF, DOCX, and TXT",
            )

        content = await upload.read(max_bytes + 1)
        if not content:
            raise HTTPException(status_code=400, detail=f"{filename}: file is empty")
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"{filename}: file exceeds {settings.max_upload_mb} MB",
            )

        try:
            text = extract_text(filename, content)
            chunks = chunk_text(text)
            embeddings = await create_embeddings(chunks, "RETRIEVAL_DOCUMENT")
            resume_id = uuid4()
            public_id, file_url = await upload_resume(str(resume_id), extension, content)

            record = ResumeRecord(
                id=resume_id,
                original_name=filename,
                cloudinary_public_id=public_id,
                file_url=file_url,
                uploaded_at=datetime.now(UTC),
                chunk_count=len(chunks),
                embedding_model=settings.gemini_embedding_model,
            )
            record.chunks = [
                ResumeChunk(chunk_number=number, text=chunk, embedding=embedding)
                for number, (chunk, embedding) in enumerate(
                    zip(chunks, embeddings, strict=True), start=1
                )
            ]
            try:
                async with SessionFactory() as session:
                    session.add(record)
                    await session.commit()
            except Exception:
                await delete_resume_asset(public_id)
                raise

            saved.append(
                ResumeSummary(
                    resume_id=str(record.id),
                    original_name=record.original_name,
                    uploaded_at=record.uploaded_at,
                    chunk_count=record.chunk_count,
                )
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=f"{filename}: {error}") from error
        except AIProviderError as error:
            raise HTTPException(status_code=503, detail=str(error)) from error

    return UploadResponse(resumes=saved)


@app.delete("/api/resumes/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_resume(resume_id: str) -> None:
    try:
        valid_id = UUID(resume_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="Invalid resume ID") from error

    async with SessionFactory() as session:
        record = await session.get(ResumeRecord, valid_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        await delete_resume_asset(record.cloudinary_public_id)
        await session.delete(record)
        await session.commit()


@app.post("/api/questions", response_model=QuestionResponse)
async def ask_question(body: QuestionRequest) -> QuestionResponse:
    """Retrieve relevant resume chunks and ask Gemini for a grounded answer."""
    try:
        question_embedding = (
            await create_embeddings([body.question], "RETRIEVAL_QUERY")
        )[0]
        sources = await retrieve(
            question_embedding=question_embedding,
            resume_ids=body.resume_ids,
            top_k=body.top_k or settings.top_k,
        )
        if not sources:
            raise HTTPException(status_code=400, detail="Selected resumes contain no chunks")

        answer = await generate_answer(body.question, build_context(sources))
        return QuestionResponse(answer=answer, sources=sources)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except AIProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.post("/api/questions/stream")
async def ask_question_stream(body: QuestionRequest) -> StreamingResponse:
    """Retrieve context, then stream newline-delimited JSON events to React."""
    try:
        question_embedding = (
            await create_embeddings([body.question], "RETRIEVAL_QUERY")
        )[0]
        sources = await retrieve(
            question_embedding=question_embedding,
            resume_ids=body.resume_ids,
            top_k=body.top_k or settings.top_k,
        )
        if not sources:
            raise HTTPException(status_code=400, detail="Selected resumes contain no chunks")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except AIProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    async def events():
        yield json.dumps({
            "type": "sources",
            "sources": [source.model_dump(mode="json") for source in sources],
        }) + "\n"
        try:
            async for text in stream_answer(body.question, build_context(sources)):
                yield json.dumps({"type": "token", "text": text}) + "\n"
            yield json.dumps({"type": "done"}) + "\n"
        except AIProviderError as error:
            yield json.dumps({"type": "error", "detail": str(error)}) + "\n"

    return StreamingResponse(
        events(),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# Keep this mount after the API routes. The compiled React app and the API are
# served by the same FastAPI process, so no separate frontend deployment exists.
app.mount(
    "/app",
    StaticFiles(directory=PROJECT_DIR / "frontend" / "dist", html=True, check_dir=False),
    name="react-app",
)
