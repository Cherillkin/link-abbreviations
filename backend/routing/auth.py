from fastapi import APIRouter, Depends, Request, Response

from sqlalchemy.orm import Session

from backend.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.services.auth import AuthService
from backend.databases.postgres import get_db
from backend.schemas.auth import RegisterUser, LoginUser, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_service() -> AuthService:
    raise RuntimeError("AuthService dependency not provided")

@router.post("/sign-up", responses={400: {"description": "Bad request"}},
             response_model=TokenResponse, description="Регистрация пользователя")
async def SignUp(user: RegisterUser, db: Session = Depends(get_db),
                 auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(user, db)

@router.post("/sign-in", responses={400: {"description": "Bad request"}},
             response_model=TokenResponse, description="Авторизация пользователя")
async def SignIn(user: LoginUser, db: Session = Depends(get_db), response: Response = None,
                 auth_service: AuthService = Depends(get_auth_service)):
    token = auth_service.login_user(user, db)

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    return token

@router.post("/logout", responses={400: {"description": "Bad request"}}, description="Выход")
async def Logout(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    token = request.cookies.get("access_token")
    if not token:
        return {"message": "No token found"}

    auth_service.logout_user(token)

    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
