from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Company, Job, Source, SourcePosting
from app.schemas import NormalizedJob
from app.services.normalization import normalize_text


async def upsert_job(session: AsyncSession, event: NormalizedJob) -> Job:
    source = await session.scalar(select(Source).where(Source.name == event.source_name))
    if source is None:
        source = Source(name=event.source_name)
        session.add(source)
        await session.flush()

    company_name = normalize_text(event.company_name)
    company = await session.scalar(select(Company).where(Company.normalized_name == company_name))
    if company is None:
        company = Company(name=event.company_name.strip(), normalized_name=company_name)
        session.add(company)
        await session.flush()

    posting = await session.scalar(
        select(SourcePosting).where(
            SourcePosting.source_id == source.id,
            SourcePosting.source_job_id == event.source_job_id,
        )
    )
    now = datetime.now(UTC)

    if posting:
        job = await session.get(Job, posting.job_id)
        assert job is not None
        _update_job(job, event, company.id, now)
        posting.source_url = event.source_url
        posting.apply_url = event.apply_url
        posting.raw_payload = event.raw_payload
        posting.last_seen_at = now
        posting.is_active = True
        return job

    job = Job(
        company_id=company.id,
        title=event.title.strip(),
        normalized_title=normalize_text(event.title),
        description=event.description,
        location_text=event.location_text,
        workplace_type=event.workplace_type,
        employment_type=event.employment_type,
        posted_at=event.posted_at,
        last_seen_at=now,
    )
    session.add(job)
    await session.flush()

    session.add(
        SourcePosting(
            job_id=job.id,
            source_id=source.id,
            source_job_id=event.source_job_id,
            source_url=event.source_url,
            apply_url=event.apply_url,
            raw_payload=event.raw_payload,
            last_seen_at=now,
        )
    )
    return job


def _update_job(job: Job, event: NormalizedJob, company_id, seen_at: datetime) -> None:
    job.company_id = company_id
    job.title = event.title.strip()
    job.normalized_title = normalize_text(event.title)
    job.description = event.description
    job.location_text = event.location_text
    job.workplace_type = event.workplace_type
    job.employment_type = event.employment_type
    job.posted_at = event.posted_at
    job.last_seen_at = seen_at
    job.is_active = True
