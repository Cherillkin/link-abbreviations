from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class ShortLinkCreate(BaseModel):
    original_url: HttpUrl
    custom_code: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_protected: Optional[bool] = False
    password: Optional[str] = None


class ShortLinkInfo(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: Optional[datetime]
