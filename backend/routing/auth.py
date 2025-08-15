from fastapi import APIRouter, Depends, Request, Response, status

from sqlalchemy.orm import Session

from typing import Dict, Union
from backend.models.auth import User
from backend.config.config import settings
from backend.repositories.auth import AuthRepository
from backend.services.auth import AuthService
from backend.databases.postgres import get_db
from backend.schemas.auth import RegisterUser, LoginUser, TokenResponse
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = AuthRepository()
    return AuthService(repository)


@router.post(
    "/create",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}},
    response_model=TokenResponse,
    description="Создание администратора",
)
async def create_admin(
    user_data: RegisterUser,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(get_current_user),
) -> Union[TokenResponse, dict]:
    if current_user.id_role != 1:
        return {"error": "Недостаточно прав"}
    return await auth_service.register_user(user_data, db, id_role=1)


@router.post(
    "/sign-up",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}},
    response_model=TokenResponse,
    description="Регистрация пользователя",
)
async def sign_up(
    user: RegisterUser,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.register_user(user, db)


@router.post(
    "/sign-in",
    response_model=TokenResponse,
    description="Авторизация пользователя",
)
async def sign_in(
    user: LoginUser,
    response: Response,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    token = await auth_service.login_user(user, db)

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
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> Dict[str, str]:
    token = request.cookies.get("access_token")
    if not token:
        return {"message": "No token found"}

    await auth_service.logout_user(token)
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
