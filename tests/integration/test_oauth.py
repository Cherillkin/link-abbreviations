import os
import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

# Фейковые переменные окружения для OAuth
os.environ["GOOGLE_CLIENT_ID"] = "fake_id"
os.environ["GOOGLE_CLIENT_SECRET"] = "fake_secret"
os.environ["YANDEX_CLIENT_ID"] = "fake_id"
os.environ["YANDEX_CLIENT_SECRET"] = "fake_secret"


@pytest.fixture
def mock_oauth() -> pytest.FixtureRequest:
    with patch("backend.routing.oauth.oauth") as mock:
        mock.create_client.return_value.authorize_redirect = AsyncMock(
            return_value="redirect_url"
        )
        mock.create_client.return_value.authorize_access_token = AsyncMock(
            return_value={"userinfo": {"id": "123", "email": "test@example.com"}}
        )
        mock.create_client.return_value.parse_id_token = AsyncMock(
            return_value={"id": "123", "email": "test@example.com"}
        )
        mock.create_client.return_value.get = AsyncMock(
            return_value=AsyncMock(
                json=AsyncMock(
                    return_value={"id": "123", "email": "test@example.com"}
                )
            )
        )
        yield mock


@pytest.fixture(autouse=True)
def mock_auth_service() -> pytest.FixtureRequest:
    with patch("backend.routing.oauth.AuthService") as mock:
        mock.return_value.login_oauth_user.return_value = type(
            "Token", (), {"access_token": "fake_token", "id_role": 1}
        )()
        yield mock


@pytest.fixture
def client(mock_oauth: pytest.FixtureRequest, mock_auth_service: pytest.FixtureRequest) -> TestClient:
    from backend.cmd.main import app
    return TestClient(app)


def test_oauth_login_supported_provider_google(client: TestClient) -> None:
    response = client.get("/oauth/login/google")
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_307_TEMPORARY_REDIRECT)


def test_oauth_login_supported_provider_yandex(client: TestClient) -> None:
    response = client.get("/oauth/login/yandex")
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_307_TEMPORARY_REDIRECT)


def test_oauth_login_unsupported_provider_unknown(client: TestClient) -> None:
    response = client.get("/oauth/login/unknown")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"error": "Unsupported provider"}
