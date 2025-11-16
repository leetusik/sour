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

    if not new_stock_ids:
        logger.warning("PIPELINE: No stocks to process. Finishing early.")
        return

    # 1. Create a "group" of gathering daily prices tasks to run.
    get_prices_tasks = group(
        task_fetch_daily_prices.s(stock_id) for stock_id in new_stock_ids
    )

    # 2. Create a "group" of preprocessing tasks to run.
    preprocessing_prices_tasks = group(
        task_preprocess_daily_prices.s(stock_id) for stock_id in new_stock_ids
    )

    price_chain = chain(get_prices_tasks, preprocessing_prices_tasks)
    price_chain_chord = chord(price_chain, task_notify_completion.s())

    # 3. Create a "group" of financial statement gathering tasks to run.
    get_financial_statements_tasks = group(
        task_fetch_financial_statements.s(stock_id) for stock_id in new_stock_ids
    )

    # 4. Create a "group" of financial statement preprocessing tasks to run.
    preprocessing_financial_statements_tasks = group(
        task_preprocess_financial_statements.s(stock_id) for stock_id in new_stock_ids
    )

    financial_statement_chain = chain(
        get_financial_statements_tasks, preprocessing_financial_statements_tasks
    )
    financial_statement_chain_chord = chord(
        financial_statement_chain, task_notify_completion.s()
    )

    # 5. Create a "chord" - This runs the price chain and the financial statement chain, and when both are finished, it calls the 'task_notify_completion' callback.
    pipeline = chain(price_chain_chord, financial_statement_chain_chord)
    pipeline.apply_async()


@celery_app.task
def daily_task_run_master_pipeline():
    """
    Run the daily task pipeline.
    """

    logger.info("Celery: Daily task pipeline started...")
    asyncio.run(_daily_task_run_master_pipeline_async())
