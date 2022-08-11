import pytest
from faker import Faker
from httpx import AsyncClient

from src.main import app

fake = Faker()


@pytest.fixture()
async def get_token():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        request_body = {"username": "user", "password": "User123$"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = await client.post("/auth/login", data=request_body, headers=headers)
        data = response.json()
        return data["access_token"]


# ----- GET Profile -----
async def test_returns_a_profile_when_existing_username_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        username = "user"

        # Act
        response = await client.get(f"/profiles/{username}")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["username"] == username


async def test_raises_user_not_found_exception_when_a_not_existing_username_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        fake_username = "fake_username"

        # Act
        response = await client.get(f"/profiles/{fake_username}")
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert data["detail"] == f"The user identified by id: {fake_username} could not be found."


# ----- Follow -----
async def test_returns_follow_relation_when_current_user_follows_another_user(get_token):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        username = "user_update"
        token = await get_token
        headers = {'Authorization': f"Bearer {token}"}

        # Act
        response = await client.post(f"/profiles/{username}/follow", headers=headers)
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data == {'username': 'user_update', 'follower': 'user'}


async def test_returns_follow_relation_not_found_when_there_is_no_follow_relation(get_token):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        token = await get_token
        headers = {'Authorization': f"Bearer {token}"}
        username = "not_an_user"

        # Act
        response = await client.delete(f"/profiles/{username}/unfollow", headers=headers)
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert data["detail"] == "The follow relation was not found."
