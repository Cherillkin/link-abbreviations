from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

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
async def SignIn(user: LoginUser, db: Session = Depends(get_db),
                 auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login_user(user, db)