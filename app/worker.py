from celery import Celery
from app.config import settings

# Initialize the Celery app
celery_app = Celery(
    "tasks",  # This name doesn't really matter
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND_URL,
)

# This tells Celery to automatically find any tasks.py files
# in your apps (e.g., app/tasks.py)
celery_app.autodiscover_tasks(['app'])

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
)