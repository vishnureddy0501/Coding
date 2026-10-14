from uuid import UUID

from sqlalchemy import select

from app.database import ResumeChunk, ResumeRecord, SessionFactory
from app.models import RetrievedSource


async def retrieve(
    question_embedding: list[float],
    resume_ids: list[str],
    top_k: int,
) -> list[RetrievedSource]:
    """Run cosine vector search in Neon for only the selected resumes."""
    try:
        unique_ids = [UUID(value) for value in dict.fromkeys(resume_ids)]
    except ValueError as error:
        raise ValueError("One or more resume IDs are invalid") from error

    distance = ResumeChunk.embedding.cosine_distance(question_embedding)
    statement = (
        select(ResumeChunk, ResumeRecord, distance.label("distance"))
        .join(ResumeRecord, ResumeRecord.id == ResumeChunk.resume_id)
        .where(ResumeChunk.resume_id.in_(unique_ids))
        .order_by(distance)
        .limit(top_k)
    )
    async with SessionFactory() as session:
        rows = (await session.execute(statement)).all()

    return [
        RetrievedSource(
            resume_id=str(resume.id),
            resume_name=resume.original_name,
            chunk_number=chunk.chunk_number,
            score=round(1 - float(distance_value), 4),
            text=chunk.text,
        )
        for chunk, resume, distance_value in rows
    ]


def build_context(sources: list[RetrievedSource]) -> str:
    """Label chunks so the chat model knows which resume supplied each fact."""
    return "\n\n".join(
        f"[Resume: {source.resume_name}; chunk {source.chunk_number}]\n{source.text}"
        for source in sources
    )
