from celery import Celery

from backend.config.config import CELERY_BROKER_URL, CELERY_BROKER_BACKEND

celery = Celery(
    "shortlinks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_BACKEND,
    include=[
        "backend.tasks.shortlinks",
    ]
)

celery.conf.beat_schedule = {
    "delete-expired-links-every-hour": {
        "task": "backend.tasks.maintenance.delete_expired_links",
        "schedule": 3600.0,
    },
}

celery.conf.timezone = "UTC"