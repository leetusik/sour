from celery import Celery
from celery.signals import worker_process_init
from app.config import settings

# Initialize the Celery app
celery_app = Celery(
    "tasks",  # This name doesn't really matter
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND_URL,
)

# This tells Celery to automatically find any tasks.py files
# in your apps (e.g., app/tasks.py)
celery_app.autodiscover_tasks(["app"])

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
)


# Fix for async database connections in forked worker processes
@worker_process_init.connect
def init_worker_process(**kwargs):
    """
    Dispose of the database engine when a new worker process is created.
    This ensures each worker gets fresh database connections that work
    with their own asyncio event loop.
    """
    from app.db.session import engine

    # For async engines, we need to dispose the sync engine
    engine.sync_engine.dispose()
