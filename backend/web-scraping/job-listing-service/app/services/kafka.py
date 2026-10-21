import asyncio
import json

from kafka import KafkaProducer

from app.core.config import get_settings
from app.schemas import NormalizedJob


class JobEventProducer:
    def __init__(self) -> None:
        self._producer: KafkaProducer | None = None

    async def start(self) -> None:
        settings = get_settings()
        self._producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda value: json.dumps(value, default=str).encode("utf-8"),
            acks="all",
            retries=5,
        )

    async def stop(self) -> None:
        if self._producer:
            await asyncio.to_thread(self._producer.flush)
            await asyncio.to_thread(self._producer.close)

    async def publish(self, job: NormalizedJob) -> None:
        if not self._producer:
            raise RuntimeError("Kafka producer is not started")
        settings = get_settings()
        future = self._producer.send(
            settings.kafka_job_topic,
            job.model_dump(mode="json"),
            key=f"{job.source_name}:{job.source_job_id}".encode(),
        )
        await asyncio.to_thread(future.get, timeout=15)


job_event_producer = JobEventProducer()
