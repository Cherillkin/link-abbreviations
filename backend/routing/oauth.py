from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
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
    redirect_uri = request.url_for("oauth_callback", provider=provider)
    return await oauth.create_client(provider).authorize_redirect(
        request, str(redirect_uri)
    )


@router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    request: Request,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> RedirectResponse:
    if provider not in ["google", "yandex"]:
        return {"error": "Unsupported provider"}

    token = await oauth.create_client(provider).authorize_access_token(request)

    user_info = token.get("userinfo")
    if not user_info:
        if provider == "google":
            user_info = await oauth.create_client(provider).parse_id_token(
                request, token
            )
        elif provider == "yandex":
            resp = await oauth.create_client(provider).get(
                "https://login.yandex.ru/info", token=token
            )
            user_info = resp.json()

    jwt_token = auth_service.login_oauth_user(user_info, db)

    response = RedirectResponse(url="/")
    response.set_cookie(
        "access_token", jwt_token.access_token, httponly=True, max_age=3600
    )
    return response
