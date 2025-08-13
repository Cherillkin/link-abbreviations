from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models.auth import User
from backend.schemas.auth import RegisterUser, LoginUser
from backend.utils.auth import hash_password, verify_password


class AuthRepository:
    def register_user(self, user_data: RegisterUser, db: Session) -> User:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        hashed_password = hash_password(user_data.password)

        try:
            user = User(
                email=user_data.email,
                password=hashed_password,
                id_role=2,
                created_at=datetime.utcnow(),
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error to register user: {str(e)}",
            )

        return user

    def login_user(self, user_data: LoginUser, db: Session) -> User:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or Password incorrect",
            )

        return user
