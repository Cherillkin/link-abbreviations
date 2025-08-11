from datetime import datetime, timedelta
from unittest.mock import MagicMock
import pytest
from starlette.testclient import TestClient
from fastapi import HTTPException
from jose import jwt

from backend.cmd.main import app
from backend.config.config import JWT_SECRET, ALGORITHM
from backend.routing.auth import get_auth_service
from backend.schemas.auth import TokenResponse


@pytest.fixture
def mock_auth_service():
    return MagicMock()


@pytest.fixture
def override_dependencies(mock_auth_service):
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_signup_success(mock_auth_service, override_dependencies):
    user_data = {"email": "test@example.com", "password": "password123"}
    token_response = {"access_token": "fake_token", "token_type": "bearer"}

    mock_auth_service.register_user.return_value = token_response

    response = client.post("/auth/sign-up", json=user_data)

    assert response.status_code == 200
    assert response.json() == token_response
    mock_auth_service.register_user.assert_called_once()


def test_signup_user_exists(mock_auth_service, override_dependencies):
    user_data = {"email": "exists@example.com", "password": "password123"}

    mock_auth_service.register_user.side_effect = HTTPException(
        status_code=400,
        detail="User already exists"
    )

    response = client.post("/auth/sign-up", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_signin_success(mock_auth_service, override_dependencies):
    user_data = {"email": "test@example.com", "password": "password123"}
    token_response = TokenResponse(access_token="fake_token", token_type="bearer")

    mock_auth_service.login_user.return_value = token_response

    response = client.post("/auth/sign-in", json=user_data)

    assert response.status_code == 200
    assert response.json() == token_response.model_dump()
    assert "access_token" in response.cookies
    mock_auth_service.login_user.assert_called_once()


def test_signin_fail_wrong_credentials(mock_auth_service, override_dependencies):
    user_data = {"email": "wrong@example.com", "password": "wrongpass"}

    mock_auth_service.login_user.side_effect = HTTPException(
        status_code=401,
        detail="Email or Password incorrect"
    )

    response = client.post("/auth/sign-in", json=user_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Email or Password incorrect"


def create_test_token():
    payload = {
        "sub": "test@example.com",
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


@pytest.fixture
def client_with_deps(override_dependencies):
    return TestClient(app)

def test_logout_success(mock_auth_service, client_with_deps):
    token = create_test_token()

    mock_auth_service.logout_user.return_value = None

    client_with_deps.cookies.set("access_token", token)
    response = client_with_deps.post("/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}

    mock_auth_service.logout_user.assert_called_once_with(token)


def test_logout_no_token(mock_auth_service, override_dependencies):
    client.cookies.clear()

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"message": "No token found"}
