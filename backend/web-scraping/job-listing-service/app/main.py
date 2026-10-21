import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.connectors.naukri import NaukriConnector
from app.core.logging import configure_logging
from app.database import get_session, ping_database
from app.models import Company, IngestionRun, Job, Source, SourcePosting
from app.schemas import IngestionResponse, JobListResponse, JobResponse
from app.services.kafka import job_event_producer

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await job_event_producer.start()
    logger.info("API started; Kafka producer is connected")
    yield
    await job_event_producer.stop()


app = FastAPI(title="Job Listing Service", version="0.1.0", lifespan=lifespan)


@app.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def readiness() -> dict[str, str]:
    try:
        await ping_database()
    except Exception as error:
        raise HTTPException(status_code=503, detail="Database is unavailable") from error
    return {"status": "ready"}


@app.post("/api/v1/ingestion/naukri", response_model=IngestionResponse, status_code=202)
async def ingest_naukri(
    query: str = Query(min_length=2, max_length=100),
    session: AsyncSession = Depends(get_session),
) -> IngestionResponse:
    run = IngestionRun(source_name="naukri", query=query, status="running")
    session.add(run)
    await session.commit()
    await session.refresh(run)

    try:
        jobs = await NaukriConnector().collect(query)
        for job in jobs:
            await job_event_producer.publish(job)

        run.status = "published"
        run.jobs_found = len(jobs)
        run.finished_at = datetime.now(UTC)
        await session.commit()
        return IngestionResponse(run_id=run.id, source="naukri", jobs_published=len(jobs))
    except Exception as error:
        logger.exception("Naukri ingestion failed")
        run.status = "failed"
        run.error_message = str(error)
        run.finished_at = datetime.now(UTC)
        await session.commit()
        raise HTTPException(status_code=502, detail="Naukri collection failed") from error


@app.get("/api/v1/jobs", response_model=JobListResponse)
async def list_jobs(
    q: str | None = Query(default=None, max_length=100),
    location: str | None = Query(default=None, max_length=100),
    workplace_type: str | None = Query(default=None, max_length=30),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> JobListResponse:
    statement = (
        select(Job, Company, SourcePosting, Source)
        .join(Company, Job.company_id == Company.id)
        .join(SourcePosting, SourcePosting.job_id == Job.id)
        .join(Source, SourcePosting.source_id == Source.id)
        .where(Job.is_active.is_(True), SourcePosting.is_active.is_(True))
        .order_by(Job.posted_at.desc().nullslast(), Job.first_seen_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    if q:
        term = f"%{q.strip().lower()}%"
        statement = statement.where(or_(Job.normalized_title.ilike(term), Job.description.ilike(term)))
    if location:
        statement = statement.where(Job.location_text.ilike(f"%{location.strip()}%"))
    if workplace_type:
        statement = statement.where(Job.workplace_type == workplace_type.lower())

    rows = (await session.execute(statement)).all()
    items = [
        JobResponse(
            id=job.id,
            title=job.title,
            company_name=company.name,
            location_text=job.location_text,
            workplace_type=job.workplace_type,
            employment_type=job.employment_type,
            description=job.description,
            apply_url=posting.apply_url,
            posted_at=job.posted_at,
            source_name=source.name,
        )
        for job, company, posting, source in rows
    ]
    return JobListResponse(items=items, page=page, limit=limit)
