from fastapi.testclient import TestClient
from src.main import app
from faker import Faker

fake = Faker()


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/auth/signup",
        json={
            "username": fake.pystr(),
            "password": fake.password()
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == user_id
