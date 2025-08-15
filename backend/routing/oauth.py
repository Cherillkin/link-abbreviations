from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse

from backend.config.config import settings
from backend.config.oauth import oauth
from backend.services.auth import AuthService
from backend.repositories.auth import AuthRepository
from backend.databases.postgres import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/oauth", tags=["OAuth"])


def get_auth_service() -> AuthService:
    return AuthService(AuthRepository())


@router.get("/login/{provider}")
async def oauth_login(provider: str, request: Request) -> RedirectResponse:
    if provider not in ["google", "yandex"]:
        return {"error": "Unsupported provider"}
    redirect_uri = f"{settings.backend_url}/oauth/callback/{provider}"
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> RedirectResponse:
    if provider not in ["google", "yandex"]:
        return {"error": "Unsupported provider"}

    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)

    user_info = token.get("userinfo")
    if not user_info:
        if provider == "google":
            user_info = await client.parse_id_token(request, token)
        elif provider == "yandex":
            resp = await client.get("https://login.yandex.ru/info", token=token)
            user_info = resp.json()

    jwt_token = auth_service.login_oauth_user(user_info, db)

    response.set_cookie(
        key="access_token",
        value=jwt_token.access_token,
        httponly=False,
        samesite="lax",
        max_age=3600 * 24 * 7,
    )
    response.set_cookie(
        key="id_role",
        value=str(jwt_token.id_role),
        httponly=False,
        samesite="lax",
        max_age=3600 * 24 * 7,
    )

    frontend_redirect = f"{settings.frontend_url}/"
    return RedirectResponse(url=frontend_redirect, status_code=302)
