from fastapi.testclient import TestClient
from faker import Faker

from src.main import app

fake = Faker()


client = TestClient(app)


# ----- SignUp -----
def test_create_an_user_when_a_valid_username_and_password_is_given():
    # Arrange
    username = fake.pystr()
    password = fake.password()

    # Act
    response = client.post("/auth/signup", json={"username": username, "password": password})
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["username"] == username


def test_raise_invalid_password_when_an_invalid_password_is_given():
    # Arrange
    username = fake.pystr()
    password = "weakPassword"

    # Act
    response = client.post("/auth/signup", json={"username": username, "password": password})
    data = response.json()
    message = data["detail"][0]

    # Assert
    assert response.status_code == 422
    assert message["msg"] == "Password must contain a minimum of 8 characters, at least one digit, one uppercase, " \
                             "one lowercase and one symbol"


# ----- Login -----
def test_returns_the_user_username_when_valid_credentials_are_given():
    # Arrange
    request_body = {"username": "arthur", "password": "Arthur123$"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Act
    response = client.post("/auth/login", data=request_body, headers=headers)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "access_token" in data


def test_raise_invalid_password_when_wrong_password_is_given():
    # Arrange
    request_body = {"username": "arthur", "password": "invalidpassword"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Act
    response = client.post("/auth/login", data=request_body, headers=headers)
    data = response.json()

    # Assert
    assert response.status_code == 401
    assert data["detail"] == "Password is invalid."
