from fastapi import APIRouter
from app.tasks.stock_tasks import daily_task_run_master_pipeline

# 1. Create a router for this resource
router = APIRouter()


@router.post("/daily_task_pipeline", status_code=202)
async def create_daily_task_pipeline():
    """
    Run the daily task pipeline.
    """

    daily_task_run_master_pipeline.delay()

    return {"message": "Daily task pipeline has been started."}
