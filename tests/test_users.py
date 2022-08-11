from faker import Faker
from httpx import AsyncClient

from src.main import app

fake = Faker()


# ----- Get User -----
async def test_returns_user_when_existing_id_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        uuid = "30e30b31-fa93-487f-b000-edaaa69f050f"

        # Act
        response = await client.get(f"/users/{uuid}")
        user = response.json()

        # Assert
        assert response.status_code == 200
        assert user["id"] == uuid


async def test_raises_not_found_exception_when_a_not_existing_id_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        false_uuid = "2"

        # Act
        response = await client.get(f"/users/{false_uuid}")
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert data["detail"] == f"The user identified by id: {false_uuid} could not be found."


# ----- Update User -----
async def test_returns_updated_user_when_existing_id_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        uuid = "01ad956f-cb73-424e-bb33-a38736486488"
        user_update = {
            "username": "user_update",
            "bio": fake.pystr()
        }

        # Act
        response = await client.put(f"/users/{uuid}", json=user_update)
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["bio"] == user_update["bio"]


async def test_raises_not_found_exception_when_a_not_existing_id_is_given_to_update():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        false_uuid = "2"
        fake_user = {
            "username": "user_update",
        }

        # Act
        response = await client.put(f"/users/{false_uuid}", json=fake_user)
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert data["detail"] == f"The user identified by id: {false_uuid} could not be found."
