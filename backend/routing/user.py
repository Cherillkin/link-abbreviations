from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.databases.postgres import get_db
from backend.repositories.user import UserRepository
from backend.schemas.auth import UserBase
from backend.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])

def get_user_service() -> UserService:
    return UserService(UserRepository())

@router.get("/{client_id}", responses={400: {"description": "Bad Request"}}, response_model=UserBase, description="Получение пользователя")
def get_client(client_id: int, db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.get_user(db, client_id)

