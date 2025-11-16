from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stocks import Stock
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


async def create_stock(session: AsyncSession, new_stock: Stock) -> Stock:
    logger.info("Crud stock: Creating stock...")
    try:
        session.add(new_stock)
        await session.commit()
        logger.info("Crud stock: Created stock.")
        return new_stock
    except Exception as e:
        logger.error(f"Crud stock: Failed to create stock. Error: {e}")
        raise e


async def delete_all_stocks(session: AsyncSession):
    logger.info("Crud stock: Deleting all stocks...")
    try:
        result = await session.execute(select(Stock))
        for stock in result.scalars().all():
            await session.delete(stock)
        await session.commit()
        logger.info("Crud: Deleted all stocks.")
    except Exception as e:
        logger.error(f"Crud: Failed to delete all stocks. Error: {e}")
        raise e
