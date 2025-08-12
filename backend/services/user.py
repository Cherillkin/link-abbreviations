from sqlalchemy.orm import Session

from backend.repositories.user import UserRepository
from backend.schemas.auth import UserBase


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, db: Session, client_id: int) -> UserBase:
        user = self.repository.get_user_by_id(db, client_id)
        return user
