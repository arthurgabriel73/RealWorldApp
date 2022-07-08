from functools import lru_cache

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from src.core.configs import settings

__engine: AsyncEngine = create_async_engine(settings.DB_URL)


Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=__engine
)


@lru_cache()
def db_engine_factory():
    return __engine
