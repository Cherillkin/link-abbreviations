from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str


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
