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
    expires_at: Optional[datetime]
    is_protected: Optional[bool] = None


class ShortLinkInfoWithClick(ShortLinkInfo):
    created_at: datetime
    click_count: Optional[int] = None
    is_protected: Optional[bool] = None