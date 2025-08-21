from datetime import datetime

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List, Union, Dict

from backend.config.config import settings
from backend.databases.redis_db import redis_client
from backend.models.auth import User
from backend.models.shortLink import ShortLink
from backend.repositories.shortLinks import ShortLinkRepository
from backend.schemas.shortLink import ShortLinkCreate, ShortLinkInfoWithClick
from backend.tasks.shortlinks import log_click_task
from backend.utils.shortlink import (
    generate_unique_code,
    check_link_limit,
    validate_custom_code,
)


class ShortLinkService:
    def __init__(self, repository: ShortLinkRepository):
        self.repository = repository

    def create(self, db: Session, user: User, data: ShortLinkCreate) -> ShortLink:
        check_link_limit(user.id_user, limit=settings.daily_link_limit)

        code = data.custom_code or generate_unique_code(db)

        if data.custom_code:
            validate_custom_code(code)

        if redis_client.exists(code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Short code is already used (cached)",
            )

        if self.repository.is_code_taken(db, code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code is already using"
            )

        try:
            link = ShortLink(
                original_url=str(data.original_url),
                short_code=code,
                id_creator=user.id_user,
                expires_at=data.expires_at,
                is_protected=data.is_protected,
                password=data.password,
            )

            created_link = self.repository.create(db, link)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error to register user: {str(e)}",
            )

        redis_client.setex(code, settings.cache_ttl, created_link.original_url)

        return created_link

    def get_info(self, db: Session, code: str) -> ShortLinkInfoWithClick:
        link = self.repository.get_by_code(db, code)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
            )

        clicks = self.repository.count_clicks(db, link.id_link)

        return ShortLinkInfoWithClick(
            short_code=link.short_code,
            original_url=link.original_url,
            created_at=link.created_at,
            expires_at=link.expires_at,
            click_count=clicks,
        )

    def get_all_links_code(self, db: Session) -> List[ShortLinkInfoWithClick]:
        links = self.repository.get_all_links_code(db)
        if not links:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List is empty"
            )

        return links

    def redirect(self, db: Session, code: str, request: Request) -> dict:
        link = self.repository.get_by_code(db, code)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
            )

        if link.expires_at and link.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="Link has expired"
            )

        if link.is_protected:
            return {"status": "protected", "is_protected": True}

        log_click_task.delay(
            link.id_link,
            request.client.host,
            request.headers.get("user-agent"),
            request.headers.get("referer"),
        )

        return {"status": "ok", "is_protected": False, "redirect_url": link.original_url}

    def get_top_links_stats(self, db: Session, limit: int = 5) -> List[Dict]:
        results = self.repository.get_top_links_last_7_days(db, limit)
        return [
            {"short_code": r[0], "original_url": r[1], "clicks": r[2]} for r in results
        ]

    def verify_password_short_link(
        self, db: Session, code: str, password: str
    ) -> Union[dict, ShortLink]:
        link = self.repository.get_by_code(db, code)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
            )

        if not link.is_protected:
            return {"status": "not_protected", "redirect_url": link.original_url}

        if link.password != password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password"
            )

        return link

    def get_user_links(self, db: Session, user: User) -> List[ShortLinkInfoWithClick]:
        links = self.repository.get_by_user(db, user.id_user)
        return [
            ShortLinkInfoWithClick(
                short_code=link.short_code,
                original_url=link.original_url,
                created_at=link.created_at,
                expires_at=link.expires_at,
                click_count=self.repository.count_clicks(db, link.id_link),
            )
            for link in links
        ]

    def delete_user_link(self, db: Session, user: User, code: str) -> dict:
        link = self.repository.get_by_code(db, code)
        if not link or link.id_creator != user.id_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Link not found or you do not have permission to delete it",
            )
        self.repository.delete(db, link)
        return {"status": "deleted", "short_code": code}
