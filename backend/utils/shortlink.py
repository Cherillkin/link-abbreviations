import re
import base64
import random
import string
import qrcode

from io import BytesIO

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.shortLink import ShortLink
from backend.databases.redis_db import redis_client
from backend.config.config import settings


def generate_unique_code(
    db: Session, length: int = settings.generate_unique_code_length
) -> str:
    characters = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(characters, k=length))
        if not db.query(ShortLink).filter_by(short_code=code).first():
            return code


def generate_qr_code(url: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=settings.qr_box_size,
        border=settings.qr_border,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def check_link_limit(user_id: int, limit: int = settings.daily_link_limit) -> None:
    key = f"link_count:{user_id}:{datetime.today().isoformat()}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, settings.link_count_ttl)
    if count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily link creation limit reached",
        )


def validate_custom_code(code: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom code can only contain letters, numbers, '-' and '_'",
        )
