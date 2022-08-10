import pytest
import asyncio
from fastapi.testclient import TestClient
from faker import Faker


from src.main import app

fake = Faker()

client = TestClient(app)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture()
def random_user():
    random_user = {"username": fake.pystr(), "password": fake.password()}
    response = client.post(f"/auth/signup", json=random_user)
    data = response.json()
    username = data["username"]

    return username


@pytest.fixture()
def token():
    request_body = {"username": "arthur", "password": "Arthur123$"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post("/auth/login", data=request_body, headers=headers)
    data = response.json()

    token = data["access_token"]

    return token


# ----- GET Profile -----
def test_returns_a_profile_when_existing_username_is_given():
    # Arrange
    username = "user"

    # Act
    response = client.get(f"/profiles/{username}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["username"] == username


def test_raise_user_not_found_exception_when_a_not_existing_username_is_given():
    # Arrange
    fake_username = "fake_username"

    # Act
    response = client.get(f"/profiles/{fake_username}")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == f"The user identified by id: {fake_username} could not be found."


# ----- Follow -----
def test_returns_follow_relation_when_current_user_follows_another_user(event_loop, token, random_user):
    # Arrange
    random_user_username = random_user["username"]
    headers = {'Authorization': f'Bearer {token}'}

    # Act
    response = client.post(f"/profiles/{random_user_username}/follow", headers=headers)
    data = response.json()

    # Assert
    assert response.status_code == 200
