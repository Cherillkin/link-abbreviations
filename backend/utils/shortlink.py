import base64
import random
import string
import qrcode
from io import BytesIO
from sqlalchemy.orm import Session

from backend.models.shortLink import ShortLink


def generate_unique_code(db: Session, length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not db.query(ShortLink).filter_by(short_code=code).first():
            return code

def generate_qr_code(url: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

