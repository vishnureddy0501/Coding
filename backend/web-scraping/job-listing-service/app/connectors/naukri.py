import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

from app.core.config import get_settings
from app.schemas import NormalizedJob


class NaukriConnector:
    """Naukri ingestion boundary.

    Sample mode is used for local end-to-end testing. Live mode deliberately
    accepts only an explicitly configured, permitted URL and parses standard
    JobPosting JSON-LD. It does not attempt to bypass access controls.
    """

    source_name = "naukri"

    async def collect(self, query: str) -> list[NormalizedJob]:
        settings = get_settings()

        if settings.naukri_mode.lower() == "sample":
            return self._sample_jobs(query)

        if not settings.naukri_search_url_template:
            raise ValueError(
                "Live Naukri mode requires NAUKRI_SEARCH_URL_TEMPLATE. "
                "Use it only after confirming automated access is permitted."
            )

        url = settings.naukri_search_url_template.format(query=quote_plus(query))
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(url, headers={"User-Agent": "JobListingService/1.0"})
            response.raise_for_status()

        jobs = self._jobs_from_json_ld(response.text, url)
        if not jobs:
            raise ValueError(
                "No JobPosting JSON-LD found. Do not add brittle bypass logic; "
                "use an approved source contract or update this connector after review."
            )
        return jobs

    def _sample_jobs(self, query: str) -> list[NormalizedJob]:
        now = datetime.now(UTC)
        return [
            NormalizedJob(
                source_job_id="sample-naukri-1001",
                title=f"{query.title()} Backend Engineer",
                company_name="Sample Technologies",
                location_text="Hyderabad, Telangana",
                workplace_type="hybrid",
                employment_type="full-time",
                description="Sample Naukri event used to test the Kafka and PostgreSQL pipeline.",
                source_url="https://www.naukri.com/sample-naukri-1001",
                apply_url="https://www.naukri.com/sample-naukri-1001",
                posted_at=now,
                raw_payload={"mode": "sample", "query": query},
            ),
            NormalizedJob(
                source_job_id="sample-naukri-1002",
                title=f"Senior {query.title()} Developer",
                company_name="Example Labs",
                location_text="Remote, India",
                workplace_type="remote",
                employment_type="full-time",
                description="Second sample Naukri event for idempotent consumer testing.",
                source_url="https://www.naukri.com/sample-naukri-1002",
                apply_url="https://www.naukri.com/sample-naukri-1002",
                posted_at=now,
                raw_payload={"mode": "sample", "query": query},
            ),
        ]

    def _jobs_from_json_ld(self, html: str, page_url: str) -> list[NormalizedJob]:
        soup = BeautifulSoup(html, "html.parser")
        records: list[dict[str, Any]] = []

        for script in soup.select('script[type="application/ld+json"]'):
            try:
                records.extend(self._flatten_json_ld(json.loads(script.string or "{}")))
            except json.JSONDecodeError:
                continue

        jobs: list[NormalizedJob] = []
        for record in records:
            if record.get("@type") != "JobPosting":
                continue

            title = str(record.get("title", "")).strip()
            company = str((record.get("hiringOrganization") or {}).get("name", "")).strip()
            source_url = str(record.get("url") or page_url)
            if not title or not company:
                continue

            source_job_id = hashlib.sha256(source_url.encode()).hexdigest()
            location = self._location_text(record.get("jobLocation"))
            jobs.append(
                NormalizedJob(
                    source_job_id=source_job_id,
                    title=title,
                    company_name=company,
                    location_text=location,
                    workplace_type="remote" if record.get("jobLocationType") == "TELECOMMUTE" else "unknown",
                    employment_type=str(record.get("employmentType", "unknown")).lower(),
                    description=str(record.get("description", "")),
                    source_url=source_url,
                    apply_url=source_url,
                    raw_payload=record,
                )
            )
        return jobs

    def _flatten_json_ld(self, value: Any) -> list[dict[str, Any]]:
        if isinstance(value, list):
            return [item for entry in value for item in self._flatten_json_ld(entry)]
        if isinstance(value, dict) and isinstance(value.get("@graph"), list):
            return [item for entry in value["@graph"] for item in self._flatten_json_ld(entry)]
        return [value] if isinstance(value, dict) else []

    def _location_text(self, value: Any) -> str:
        locations = value if isinstance(value, list) else [value]
        labels: list[str] = []
        for location in locations:
            address = (location or {}).get("address", {}) if isinstance(location, dict) else {}
            label = ", ".join(
                str(address.get(key)) for key in ("addressLocality", "addressRegion", "addressCountry") if address.get(key)
            )
            if label:
                labels.append(label)
        return " | ".join(labels)
