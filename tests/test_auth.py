import asyncio

import pytest
from httpx import AsyncClient
from faker import Faker

from src.main import app

fake = Faker()


# ----- SignUp -----
@pytest.mark.anyio
async def test_create_an_user_when_a_valid_username_and_password_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        username = fake.pystr()
        password = fake.password()

        # Act
        response = await client.post("/auth/signup", json={"username": username, "password": password})
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["username"] == username


async def test_raises_invalid_password_when_an_invalid_password_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        username = fake.pystr()
        password = "weakPassword"

        # Act
        response = await client.post("/auth/signup", json={"username": username, "password": password})
        data = response.json()
        message = data["detail"][0]

        # Assert
        assert response.status_code == 422
        assert message["msg"] == "Password must contain a minimum of 8 characters, at least one digit, one uppercase, " \
                                 "one lowercase and one symbol"


# ----- Login -----
async def test_returns_token_when_valid_credentials_are_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        request_body = {"username": "user", "password": "User123$"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Act
        response = await client.post("/auth/login", data=request_body, headers=headers)
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "access_token" in data


async def test_raises_invalid_password_when_wrong_password_is_given():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Arrange
        request_body = {"username": "user", "password": "invalidPassword"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Act
        response = await client.post("/auth/login", data=request_body, headers=headers)
        data = response.json()

        # Assert
        assert response.status_code == 401
        assert data["detail"] == "Password is invalid."
