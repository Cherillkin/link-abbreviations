import os
from typing import Generator, Any
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from backend.cmd.main import app

os.environ["GOOGLE_CLIENT_ID"] = "fake_id"
os.environ["GOOGLE_CLIENT_SECRET"] = "fake_secret"
os.environ["YANDEX_CLIENT_ID"] = "fake_id"
os.environ["YANDEX_CLIENT_SECRET"] = "fake_secret"

client = TestClient(app)


@pytest.fixture
def mock_oauth() -> Generator:
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
                json=AsyncMock(return_value={"id": "123", "email": "test@example.com"})
            )
        )
        yield mock


def test_oauth_login_supported_provider(mock_oauth: Any) -> None:
    response = client.get("/oauth/login/google")
    assert response.status_code == 200 or response.status_code == 307


def test_oauth_login_unsupported_provider() -> None:
    response = client.get("/oauth/login/unknown")
    assert response.status_code == 200
    assert response.json() == {"error": "Unsupported provider"}
