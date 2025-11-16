import asyncio
from app.worker import celery_app  # Import the Celery app
from app.db.session import AsyncSessionLocal


async def _daily_task_run_master_pipeline_async():
    """
    Run the daily task pipeline.
    """

    # async with AsyncSessionLocal() as session:


@celery_app.task
def daily_task_run_master_pipeline():
    """
    Run the daily task pipeline.
    """

    print("Daily task pipeline started...")
    asyncio.run(_daily_task_run_master_pipeline_async())
