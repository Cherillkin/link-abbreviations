import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import uuid

from backend.cmd.main import app
from backend.databases.postgres import Base, get_db
from backend.models.auth import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def test_user() -> Generator[User, None, None]:
    db = TestingSessionLocal()
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = User(email=unique_email, password="hashedpass", id_role=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.query(User).filter_by(id_user=user.id_user).delete()
    db.commit()
