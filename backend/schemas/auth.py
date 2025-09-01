from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class RegisterUser(UserBase):
    password: str


class LoginUser(UserBase):
    password: str


class GetUser(UserBase):
    id_user: int
    id_role: int
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id_role: int
