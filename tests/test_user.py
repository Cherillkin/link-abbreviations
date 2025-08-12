import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.cmd.main import app
from backend.databases.postgres import Base, get_db
from backend.models.auth import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Создаём таблицы
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = User(email="test@example.com", password="hashedpass", id_role=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.query(User).delete()
    db.commit()


def test_get_existing_user(test_user):
    response = client.get(f"/user/{test_user.id_user}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_get_non_existing_user():
    response = client.get("/user/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
