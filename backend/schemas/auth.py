from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    password: str

class RegisterUser(UserBase):
    id_role: int
    created_at: datetime

class LoginUser(UserBase):
    pass

class GetUser(UserBase):
    id_user: int
    id_role: int
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"