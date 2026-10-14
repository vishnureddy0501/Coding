import asyncio
from io import BytesIO
from urllib.parse import unquote, urlparse

import cloudinary
import cloudinary.uploader

from app.config import settings


def parse_cloudinary_url(value: str) -> dict[str, str]:
    """Convert CLOUDINARY_URL into the fields expected by the Python SDK."""
    parsed = urlparse(value)
    if (
        parsed.scheme != "cloudinary"
        or not parsed.hostname
        or not parsed.username
        or not parsed.password
    ):
        raise ValueError(
            "CLOUDINARY_URL must use: cloudinary://api_key:api_secret@cloud_name"
        )

    return {
        "cloud_name": parsed.hostname,
        "api_key": unquote(parsed.username),
        "api_secret": unquote(parsed.password),
    }


def configure_cloudinary() -> None:
    """Configure the Cloudinary client from the application's .env settings."""
    if not settings.cloudinary_url:
        return  # The startup validation reports a clear missing-variable error.
    cloudinary.config(**parse_cloudinary_url(settings.cloudinary_url), secure=True)


configure_cloudinary()


async def upload_resume(
    resume_id: str,
    extension: str,
    content: bytes,
) -> tuple[str, str]:
    """Upload an original resume as an unchanged Cloudinary raw asset."""

    def _upload() -> dict:
        return cloudinary.uploader.upload(
            BytesIO(content),
            resource_type="raw",
            type="authenticated",
            public_id=f"resume-rag/{resume_id}/original{extension}",
            overwrite=False,
        )

    result = await asyncio.to_thread(_upload)
    return result["public_id"], result["secure_url"]


async def delete_resume_asset(public_id: str) -> None:
    """Delete a raw Cloudinary asset using its stored provider ID."""

    def _delete() -> None:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="raw",
            type="authenticated",
        )
        if result.get("result") not in {"ok", "not found"}:
            raise RuntimeError("Cloudinary could not delete the resume")

    await asyncio.to_thread(_delete)
