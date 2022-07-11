from functools import lru_cache
from typing import Generator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from src.config.settings import settings_factory

__engine: AsyncEngine = create_async_engine(settings_factory().DB_URL)


Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=__engine
)


async def get_session() -> Generator:
    session: AsyncSession = AsyncSession()

    try:
        yield session
    finally:
        await session.close()


@lru_cache()
def db_engine_factory():
    return __engine
