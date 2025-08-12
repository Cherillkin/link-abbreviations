from datetime import datetime

from celery.worker.state import requests

from backend.config.celery_app import celery
from backend.databases.postgres import SessionLocal
from backend.models.linkClick import LinkClick
from backend.models.shortLink import ShortLink
from backend.utils.shortlink import generate_qr_code


@celery.task
def log_click_task(id_link: int, ip: str, user_agent: str, referer: str) -> None:
    db = SessionLocal()
    try:
        click = LinkClick(
            id_link=id_link, ip_address=ip, user_agent=user_agent, referer=referer
        )
        db.add(click)
        db.commit()
    finally:
        db.close()


@celery.task
def delete_expired_links() -> None:
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        deleted_count = (
            db.query(ShortLink)
            .filter(ShortLink.expires_at != None)
            .filter(ShortLink.expires_at < now)
            .delete(synchronize_session=False)
        )
        db.commit()
        print(f"[delete_expired_links] Deleted {deleted_count} expired links")
    except Exception as e:
        print(f"[delete_expired_links] Error: {e}")
        db.rollback()
    finally:
        db.close()


@celery.task
def check_original_url(id_link: int, original_url: str) -> None:
    db = SessionLocal()
    try:
        try:
            resp = requests.head(original_url, timeout=5, allow_redirects=True)
            is_alive = resp.status_code < 400
        except Exception:
            is_alive = False

        if not is_alive:
            link = db.query(ShortLink).filter_by(id_link=id_link).first()
            if link:
                db.delete(link)
                db.commit()
                print(f"[check_original_url] Deleted dead link: {original_url}")
    finally:
        db.close()


@celery.task
def generate_qr_code_task(short_url: str) -> str:
    qr_base64 = generate_qr_code(short_url)
    return qr_base64
