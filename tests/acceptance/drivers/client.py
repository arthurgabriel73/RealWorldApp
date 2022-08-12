from functools import lru_cache
from httpx import AsyncClient
from src.main import app


@lru_cache()
async def client_factory() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://localhost:8000")
