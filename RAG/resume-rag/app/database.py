from datetime import datetime
from uuid import UUID

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.config import settings


EMBEDDING_DIMENSIONS = 768


class Base(AsyncAttrs, DeclarativeBase):
    pass


class ResumeRecord(Base):
    """Metadata for one original resume stored in Cloudinary."""

    __tablename__ = "resumes"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    original_name: Mapped[str] = mapped_column(String(255))
    cloudinary_public_id: Mapped[str] = mapped_column(String(500), unique=True)
    file_url: Mapped[str] = mapped_column(String(1000))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    chunk_count: Mapped[int] = mapped_column(Integer)
    embedding_model: Mapped[str] = mapped_column(String(100))

    chunks: Mapped[list["ResumeChunk"]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
    )


class ResumeChunk(Base):
    """Searchable text chunk and its Gemini embedding."""

    __tablename__ = "resume_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        index=True,
    )
    chunk_number: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(VECTOR(EMBEDDING_DIMENSIONS))

    resume: Mapped[ResumeRecord] = relationship(back_populates="chunks")


database_url = settings.async_database_url or (
    "postgresql+asyncpg://missing:missing@localhost/missing"
)
engine = create_async_engine(database_url, pool_pre_ping=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def initialize_database() -> None:
    """Enable pgvector and create the two small project tables."""
    async with engine.begin() as connection:
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await connection.run_sync(Base.metadata.create_all)
