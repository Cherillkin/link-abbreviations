from typing import Optional, List

from sqlalchemy.orm import Session

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

    def get_all_links_code(self, db: Session) -> List[ShortLink]:
        return db.query(ShortLink).all()
