import pytest
from faker import Faker
from httpx import AsyncClient

from src.main import app
fake = Faker()


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_create_user(anyio_backend):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/auth/signup", json={
            "username": fake.pystr(),
            "password": fake.password()
        })
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        user_id = data["id"]

        response = await client.get(f"/users/{user_id}")
        data = response.json()
        assert "id" in data
        assert data["id"] == user_id
