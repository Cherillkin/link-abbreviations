import pytest
from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from typing import Generator

from pytest_mock import MockerFixture

from backend.cmd.main import app
from backend.models import User, ShortLink
from backend.schemas.shortLink import ShortLinkInfo, ShortLinkInfoWithClick
from backend.services.shortLinks import ShortLinkService


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake_user() -> User:
    user = User(id_user=1)
    user.username = "test"
    return user


@pytest.fixture
def fake_short_link() -> ShortLink:
    return ShortLink(
        id_link=1,
        original_url="https://example.com",
        short_code="abc123",
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=1),
        is_protected=False,
        password=None,
        id_creator=1,
    )


@pytest.fixture(autouse=True)
def override_dependencies(fake_user: User) -> Generator[MagicMock, None, None]:
    app.dependency_overrides[
        __import__("backend.routing.shortLinks").routing.shortLinks.get_current_user
    ] = lambda: fake_user

    mock_service = MagicMock(spec=ShortLinkService)
    app.dependency_overrides[
        __import__(
            "backend.routing.shortLinks"
        ).routing.shortLinks.get_short_link_service
    ] = lambda: mock_service

    yield mock_service
    app.dependency_overrides.clear()


def test_create_short_link(
    client: TestClient, override_dependencies: MagicMock, fake_short_link: ShortLink
) -> None:
    override_dependencies.create.return_value = fake_short_link

    payload = {
        "original_url": "https://example.com",
        "custom_code": None,
        "expires_at": None,
        "is_protected": False,
        "password": None,
    }
    resp = client.post("/short-links/", json=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["short_code"] == fake_short_link.short_code


def test_get_link_info(
    client: TestClient, override_dependencies: MagicMock, fake_short_link: ShortLink
) -> None:
    override_dependencies.get_info.return_value = ShortLinkInfoWithClick(
        short_code=fake_short_link.short_code,
        original_url=fake_short_link.original_url,
        created_at=fake_short_link.created_at,
        expires_at=fake_short_link.expires_at,
        click_count=0,
    )
    response = client.get(f"/short-links/{fake_short_link.short_code}")
    assert response.status_code == status.HTTP_200_OK


def test_get_all_links(
    client: TestClient, override_dependencies: MagicMock, fake_short_link: ShortLink
) -> None:
    override_dependencies.get_all_links_code = MagicMock(
        return_value=[
            ShortLinkInfo(
                short_code=fake_short_link.short_code,
                original_url=fake_short_link.original_url,
                created_at=fake_short_link.created_at,
                expires_at=fake_short_link.expires_at,
            )
        ]
    )
    response = client.get("/short-links/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["short_code"] == fake_short_link.short_code


def test_redirect_to_original(
    client: TestClient, override_dependencies: MagicMock, fake_short_link: ShortLink
) -> None:
    override_dependencies.redirect.return_value = fake_short_link.original_url
    response = client.get(
        f"/short-links/r/{fake_short_link.short_code}", follow_redirects=False
    )
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == fake_short_link.original_url


def test_verify_password_not_protected(
    client: TestClient, override_dependencies: MagicMock, fake_short_link: ShortLink
) -> None:
    fake_short_link.is_protected = False

    override_dependencies.verify_password_short_link.return_value = fake_short_link
    response = client.post(
        f"/short-links/verify-password?code={fake_short_link.short_code}&password=test"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "not_protected"


def test_generate_qr_for_link(
    client: TestClient,
    override_dependencies: MagicMock,
    fake_short_link: ShortLink,
    mocker: MockerFixture,
) -> None:
    override_dependencies.get_info.return_value = fake_short_link
    fake_task = MagicMock()
    fake_task.id = "task-123"

    mocker.patch(
        "backend.routing.shortLinks.generate_qr_code_task.delay", return_value=fake_task
    )

    response = client.post(f"/short-links/{fake_short_link.short_code}/qr")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "processing"
    assert response.json()["task_id"] == "task-123"
