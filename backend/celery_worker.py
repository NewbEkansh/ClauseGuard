from celery import Celery
from backend.config import settings

celery = Celery(
    "clauseguard",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

# Proper autodiscovery
celery.autodiscover_tasks(
    packages=["backend.tasks"])