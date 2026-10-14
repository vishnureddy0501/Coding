from datetime import datetime

from pydantic import BaseModel, Field


class ResumeSummary(BaseModel):
    resume_id: str
    original_name: str
    uploaded_at: datetime
    chunk_count: int


class UploadResponse(BaseModel):
    resumes: list[ResumeSummary]


class QuestionRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1_000)
    resume_ids: list[str] = Field(min_length=1, max_length=50)
    top_k: int | None = Field(default=None, ge=1, le=15)


class RetrievedSource(BaseModel):
    resume_id: str
    resume_name: str
    chunk_number: int
    score: float
    text: str


class QuestionResponse(BaseModel):
    answer: str
    sources: list[RetrievedSource]
