import random
import string

from sqlalchemy.orm import Session

from backend.models.shortLink import ShortLink


def generate_unique_code(db: Session, length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not db.query(ShortLink).filter_by(short_code=code).first():
            return code