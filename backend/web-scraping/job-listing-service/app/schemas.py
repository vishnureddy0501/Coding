from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class NormalizedJob(BaseModel):
    source_name: str = "naukri"
    source_job_id: str
    title: str = Field(min_length=1, max_length=500)
    company_name: str = Field(min_length=1, max_length=255)
    location_text: str = ""
    workplace_type: str = "unknown"
    employment_type: str = "unknown"
    description: str = ""
    source_url: str
    apply_url: str
    posted_at: datetime | None = None
    raw_payload: dict = Field(default_factory=dict)


class IngestionResponse(BaseModel):
    run_id: UUID
    source: str
    jobs_published: int


class JobResponse(BaseModel):
    id: UUID
    title: str
    company_name: str
    location_text: str
    workplace_type: str
    employment_type: str
    description: str
    apply_url: str
    posted_at: datetime | None
    source_name: str


class JobListResponse(BaseModel):
    items: list[JobResponse]
    page: int
    limit: int
