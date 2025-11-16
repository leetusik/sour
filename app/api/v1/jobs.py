import logging
from fastapi import APIRouter, HTTPException
from app.tasks.stock_tasks import daily_task_run_master_pipeline

logger = logging.getLogger(__name__)

# 1. Create a router for this resource
router = APIRouter()


@router.post("/daily_task_pipeline", status_code=202)
async def create_daily_task_pipeline():
    """
    Run the daily task pipeline.
    """
    logger.info("API: Daily task pipeline requested. Enqueuing task...")

    try:
        daily_task_run_master_pipeline.delay()
        logger.info("API: Daily task pipeline enqueued successfully.")
        return {"message": "Daily task pipeline has been started."}

    except Exception as e:
        logger.error(f"API: Daily task pipeline failed. Error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
