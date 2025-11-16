from fastapi import APIRouter
from app.tasks.stock_tasks import run_stock_pipeline

# 1. Create a router for this resource
router = APIRouter()

@router.post("/", status_code=202)  # Path is just "/"
async def create_job():
    """
    Creates a new background job.
    In the future, this endpoint could take a body
    to decide which job to run.
    """
    
    # .delay() sends the task to Celery
    task = run_stock_pipeline.delay()
    
    # Return the task ID so the client can (optionally) track it
    return {
        "message": "Stock import job has been started.",
        "job_id": task.id
    }