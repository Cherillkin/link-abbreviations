from fastapi import APIRouter, Depends, Request, Response, status

from sqlalchemy.orm import Session

from typing import Dict
from backend.config.config import settings
from backend.services.auth import AuthService
from backend.databases.postgres import get_db
from backend.schemas.auth import RegisterUser, LoginUser, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service() -> AuthService:
    raise RuntimeError("AuthService dependency not provided")


@router.post(
    "/sign-up",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}},
    response_model=TokenResponse,
    description="Регистрация пользователя",
)
def sign_up(
    user: RegisterUser,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return auth_service.register_user(user, db)


@router.post(
    "/sign-in",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}},
    response_model=TokenResponse,
    description="Авторизация пользователя",
)
def sign_in(
    user: LoginUser,
    db: Session = Depends(get_db),
    response: Response = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    token = auth_service.login_user(user, db)

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )

    return token


@router.post(
    "/logout",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}},
    description="Выход",
)
def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> Dict[str, str]:
    token = request.cookies.get("access_token")
    if not token:
        return {"message": "No token found"}

    auth_service.logout_user(token)

    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
