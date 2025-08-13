from datetime import datetime

from sqlalchemy.orm import Session

from backend.config.config import settings
from backend.databases.redis_db import save_user_to_redis, redis_client
from backend.repositories.auth import AuthRepository
from backend.schemas.auth import RegisterUser, LoginUser, TokenResponse
from backend.utils.auth import create_access_token

from jose import jwt


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register_user(self, user_data: RegisterUser, db: Session) -> TokenResponse:
        user = self.repository.register_user(user_data, db)
        token = create_access_token(data={"sub": str(user.id_user)})

        save_user_to_redis(
            user.id_user,
            {
                "id": user.id_user,
                "email": user.email,
            },
        )

        return TokenResponse(access_token=token)

    def login_user(self, user_data: LoginUser, db: Session) -> TokenResponse:
        user = self.repository.login_user(user_data, db)
        token = create_access_token(data={"sub": str(user.id_user)})

        save_user_to_redis(
            user.id_user,
            {
                "id": user.id_user,
                "email": user.email,
            },
        )

        return TokenResponse(access_token=token)

    def logout_user(self, token: str) -> None:
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.algorithm]
            )
            exp = payload.get("exp")
            now = datetime.utcnow().timestamp()
            ttl = int(exp - now) if exp else 0
            if ttl > 0:
                redis_client.setex(f"blacklist_{token}", ttl, "true")
        except Exception:
            pass
