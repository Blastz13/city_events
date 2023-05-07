from celery import Celery
from celery.schedules import crontab

from core.config import config

celery_app = Celery(
    "celery_app",
    backend=config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)

celery_app.conf.imports = [
    "celery_app.tasks.tasks"
]
celery_app.conf.task_routes = {"celery_app.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)
celery_app.conf.beat_schedule = {
    'run-every-30-minutes': {
        'task': 'send_notifications',
        'schedule': crontab(minute='*/30'),
    },
}
