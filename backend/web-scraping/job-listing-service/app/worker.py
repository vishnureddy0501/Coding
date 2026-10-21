import asyncio
import json
import logging

from kafka import KafkaConsumer

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.database import SessionLocal
from app.schemas import NormalizedJob
from app.services.job_store import upsert_job

configure_logging()
logger = logging.getLogger(__name__)


async def run_worker() -> None:
    settings = get_settings()
    consumer = KafkaConsumer(
        settings.kafka_job_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_consumer_group,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )

    logger.info("Worker started for topic %s", settings.kafka_job_topic)
    try:
        for message in consumer:
            try:
                event = NormalizedJob.model_validate(json.loads(message.value.decode("utf-8")))
                async with SessionLocal() as session:
                    await upsert_job(session, event)
                    await session.commit()
                consumer.commit()
                logger.info("Stored source job %s", event.source_job_id)
            except Exception:
                logger.exception("Could not store Kafka event; offset is not committed")
                await asyncio.sleep(5)
    finally:
        consumer.close()


if __name__ == "__main__":
    asyncio.run(run_worker())
