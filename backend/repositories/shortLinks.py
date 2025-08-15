from datetime import datetime, timedelta
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.linkClick import LinkClick
from backend.models.shortLink import ShortLink


class ShortLinkRepository:
    def get_by_code(self, db: Session, code: str) -> Optional[ShortLink]:
        return db.query(ShortLink).filter_by(short_code=code).first()

    def is_code_taken(self, db: Session, code: str) -> bool:
        return db.query(ShortLink).filter_by(short_code=code).first() is not None

    def create(self, db: Session, link: ShortLink) -> ShortLink:
        db.add(link)
        db.commit()
        db.refresh(link)
        return link

    def count_clicks(self, db: Session, id_link: int) -> int:
        return db.query(LinkClick).filter_by(id_link=id_link).count()

    def create_click(self, db: Session, click: LinkClick) -> None:
        db.add(click)
        db.commit()

    def get_top_links_last_7_days(
        self, db: Session, limit: int = 5
    ) -> List[Tuple[str, str, int]]:
        since = datetime.utcnow() - timedelta(days=7)
        results = (
            db.query(
                ShortLink.short_code,
                ShortLink.original_url,
                func.count(LinkClick.id_click).label("clicks"),
            )
            .join(LinkClick, ShortLink.id_link == LinkClick.id_link)
            .filter(LinkClick.timestamp >= since)
            .group_by(ShortLink.id_link)
            .order_by(func.count(LinkClick.id_click).desc())
            .limit(limit)
            .all()
        )
        return results

    def get_all_links_code(self, db: Session) -> List[ShortLink]:
        return db.query(ShortLink).all()
