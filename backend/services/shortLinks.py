from datetime import datetime

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from backend.databases.redis_db import redis_client
from backend.models.auth import User
from backend.models.linkClick import LinkClick
from backend.models.shortLink import ShortLink
from backend.repositories.shortLinks import ShortLinkRepository
from backend.schemas.shortLink import ShortLinkCreate, ShortLinkInfo
from backend.utils.shortlink import generate_unique_code


class ShortLinkService:
    def __init__(self, repository: ShortLinkRepository):
        self.repository = repository

    def create(self, db: Session, user: User, data: ShortLinkCreate) -> ShortLink:
        code = data.custom_code or generate_unique_code(db)

        if redis_client.exists(code):
            raise HTTPException(status_code=400, detail="Short code is already used (cached)")

        if self.repository.is_code_taken(db, code):
            raise HTTPException(status_code=400, detail="Code is already using")

        link = ShortLink(
            original_url=str(data.original_url),
            short_code=code,
            id_creator=user.id_user,
            expires_at=data.expires_at,
            is_protected=data.is_protected,
            password=data.password
        )

        created_link = self.repository.create(db, link)

        redis_client.setex(code, 3600, created_link.original_url)

        return created_link

    def get_info(self, db: Session, code: str) -> ShortLinkInfo:
        link = self.repository.get_by_code(db, code)
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        clicks = self.repository.count_clicks(db, link.id_link)

        return ShortLinkInfo(
            short_code=link.short_code,
            original_url=link.original_url,
            created_at=link.created_at,
            expires_at=link.expires_at,
            click_count=clicks
        )

    def redirect(self, db: Session, code: str, request: Request) -> str:
        link = self.repository.get_by_code(db, code)
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        if link.expires_at and link.expires_at < datetime.utcnow():
            raise HTTPException(status_code=410, detail="Link has expired")

        if link.is_protected:
            raise HTTPException(status_code=403, detail="Password is required to access this link")

        click = LinkClick(
            id_link=link.id_link,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            referer=request.headers.get("referer")
        )

        self.repository.create_click(db, click)

        return link.original_url

    def verify_password_short_link(self, db: Session, code: str, password: str):
        link = self.repository.get_by_code(db, code)
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        if not link.is_protected:
            return {"status": "not_protected", "redirect_url": link.original_url}

        if link.password != password:
            raise HTTPException(status_code=403, detail="Invalid password")

        return link