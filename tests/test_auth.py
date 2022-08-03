from fastapi.testclient import TestClient
from unittest.mock import Mock
from faker import Faker

from src.main import app

fake = Faker()

client = TestClient(app)


def test_create_an_user_when_a_valid_username_and_password_is_given():

    username = fake.pystr()
    password = fake.password()

    response = client.post("/auth/signup", json={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username


def test_raise_invalid_password_when_an_invalid_password_is_given():
    username = fake.pystr()
    password = "weakPassword"

    response = client.post("/auth/signup", json={"username": username, "password": password})
    assert response.status_code == 422
    data = response.json()
    i = data["detail"][0]

    assert i["msg"] == "Password must contain a minimum of 8 characters, at least one digit, one uppercase, " \
                       "one lowercase and one symbol"
