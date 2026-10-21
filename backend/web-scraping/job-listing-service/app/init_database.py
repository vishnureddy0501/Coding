import asyncio

from app.database import engine
from app.models import Base


async def initialize() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(initialize())
