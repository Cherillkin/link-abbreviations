from fastapi import status
from fastapi.testclient import TestClient
from typing import Optional
import uuid
import pytest

from backend.models.auth import User
from backend.config.config import settings
from tests.conftest import TestingSessionLocal

@pytest.fixture(autouse=True)
def set_test_jwt_settings() -> None:
    settings.jwt_secret = "test-secret"
    settings.algorithm = "HS256"

def create_unique_user(email: Optional[str] = None) -> User:
    db = TestingSessionLocal()
    unique_email = email or f"test_{uuid.uuid4()}@example.com"
    user = User(email=unique_email, password="hashedpass", id_role=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_signup_and_signin(client: TestClient) -> None:
    payload = {"email": f"signup_{uuid.uuid4()}@example.com", "password": "password123"}

    response = client.post("/auth/sign-up", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    response = client.post("/auth/sign-in", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_signup_existing_user(client: TestClient) -> None:
    user = create_unique_user()

    payload = {"email": user.email, "password": "password123"}
    response = client.post("/auth/sign-up", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User already exists"
