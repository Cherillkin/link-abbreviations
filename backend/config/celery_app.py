from celery import Celery

from backend.config.config import settings

celery = Celery(
    "shortlinks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "backend.tasks.shortlinks",
    ],
)

celery.conf.beat_schedule = {
    "delete-expired-links-every-hour": {
        "task": "backend.tasks.maintenance.delete_expired_links",
        "schedule": 3600.0,
    },
}

celery.conf.timezone = "UTC"
