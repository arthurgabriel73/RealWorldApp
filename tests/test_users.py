from fastapi.testclient import TestClient
from faker import Faker

from src.main import app

fake = Faker()


client = TestClient(app)


# ----- Get User -----
def test_returns_user_when_existing_id_is_given():
    # Arrange
    uuid = "a3b27361-2005-4578-9fbd-dc8cf71363b3"

    # Act
    response = client.get(f"/users/{uuid}")
    user = response.json()

    # Assert
    assert response.status_code == 200
    assert user["id"] == uuid


def test_raises_not_found_exception_when_a_not_existing_id_is_given():
    # Arrange
    false_uuid = "2"

    # Act
    response = client.get(f"/users/{false_uuid}")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == f"The user identified by id: {false_uuid} could not be found."


# ----- Update User -----
def test_returns_updated_user_when_existing_id_is_given():
    # Arrange
    uuid = "ee23c50a-7695-417c-a79f-e6934f34b44e"
    user_update = {
        "username": "arthur_update",
        "bio": fake.pystr()
    }

    # Act
    response = client.put(f"/users/{uuid}", json=user_update)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["bio"] == user_update["bio"]


def test_raises_not_found_exception_when_a_not_existing_id_is_given_to_update():
    # Arrange
    false_uuid = "2"
    fake_user = {
        "username": "arthur_update",
    }

    # Act
    response = client.put(f"/users/{false_uuid}", json=fake_user)
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == f"The user identified by id: {false_uuid} could not be found."
