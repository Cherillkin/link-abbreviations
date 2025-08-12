from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.auth import User


class UserRepository:
    def get_user_by_id(self, db: Session, client_id: int) -> User:
        existing_client_id = db.query(User).filter(User.id_user == client_id).first()
        if not existing_client_id:
            raise HTTPException(status_code=404, detail="User not found")
        return existing_client_id
