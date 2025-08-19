import uuid
from typing import Generator, Iterator

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from backend.cmd.main import app
from backend.models.auth import User
from backend.models import ShortLink
from backend.databases.postgres import Base, get_db
from backend.routing.shortLinks import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client_with_user() -> Iterator[TestClient]:
    db = TestingSessionLocal()
    try:
        user = User(email=f"user_{uuid.uuid4()}@example.com", password="hashedpass", id_role=1)
        db.add(user)
        db.commit()
        db.refresh(user)

        app.dependency_overrides[get_current_user] = lambda: user
        client = TestClient(app)
        yield client
    finally:
        # Очистка после теста
        db.query(ShortLink).delete()
        db.query(User).filter(User.id_user == user.id_user).delete()
        db.commit()
        db.close()
        app.dependency_overrides.clear()

def test_create_and_get_short_link(client_with_user: TestClient) -> None:
    payload = {"original_url": "https://example.com"}
    response = client_with_user.post("/short-links/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    short_code = data["short_code"]
    assert short_code

    response = client_with_user.get(f"/short-links/{short_code}")
    assert response.status_code == status.HTTP_200_OK
    info = response.json()
    assert info["short_code"] == short_code
    assert info["original_url"].rstrip("/") == payload["original_url"].rstrip("/")


def test_redirect_short_link(client_with_user: TestClient) -> None:
    payload = {"original_url": "https://example.org"}
    response = client_with_user.post("/short-links/", json=payload)
    short_code = response.json()["short_code"]

    response = client_with_user.get(f"/short-links/r/{short_code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"].rstrip("/") == payload["original_url"].rstrip("/")


def test_get_all_short_links(client_with_user: TestClient) -> None:
    payload = {"original_url": "https://alltest.com"}
    client_with_user.post("/short-links/", json=payload)

    response = client_with_user.get("/short-links/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(link["original_url"].rstrip("/") == payload["original_url"].rstrip("/") for link in data)

