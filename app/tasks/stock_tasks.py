import logging
import asyncio
from app.worker import celery_app  # Import the Celery app
from app.db.session import AsyncSessionLocal
from app.crud import crud_stock
from app.services import stock_services
from app.models.stocks import Stock

logger = logging.getLogger(__name__)


async def _daily_task_run_master_pipeline_async():
    """
    Run the daily task pipeline.
    """

    new_stock_ids = []

    async with AsyncSessionLocal() as session:

        # --- Step 1: Delete all stocks (Cascade handles the rest) ---
        logger.info("Daily task pipeline: Step 1/3 - Deleting all stocks...")
        await crud_stock.delete_all_stocks(session)
        logger.info("Daily task pipeline: Step 1/3 - Deleted all stocks.")

        # --- Step 2: Get all stocks from the API ---
        logger.info(
            "Daily task pipeline: Step 2/3 - Getting all stocks from the API..."
        )
        stocks_data = await stock_services.fetch_all_stocks_from_pykrx()
        logger.info("Daily task pipeline: Step 2/3 - Got all stocks from the API.")

        # --- Step 3: Create new stocks ---
        logger.info("Daily task pipeline: Step 3/3 - Creating new stocks...")
        for stock_data in stocks_data:
            new_stock = Stock(
                name=stock_data["name"],
                ticker=stock_data["ticker"],
                market=stock_data["market"],
            )
            new_stock = await crud_stock.create_stock(session, new_stock)
            new_stock_ids.append(new_stock.id)
        logger.info("Daily task pipeline: Step 3/3 - Created new stocks.")


@celery_app.task
def daily_task_run_master_pipeline():
    """
    Run the daily task pipeline.
    """

    logger.info("Celery: Daily task pipeline started...")
    asyncio.run(_daily_task_run_master_pipeline_async())
