from typing import List, Dict, Any
from pykrx import stock
import logging

logger = logging.getLogger(__name__)


async def fetch_all_stocks_from_pykrx() -> List[Dict[str, Any]]:
    """
    Fetch all stocks from KOSPI and KOSDAQ markets using pykrx.
    Returns a list of stock data dictionaries ready for bulk creation.
    """
    logger.info("Stock services: Fetching all stocks from PyKRX...")
    stocks_to_create = []

    # Fetch KOSPI stocks
    kospi_tickers = stock.get_market_ticker_list(market="KOSPI")
    for ticker in kospi_tickers:
        name = stock.get_market_ticker_name(ticker)
        stocks_to_create.append(
            {
                "name": name,
                "ticker": ticker,
                "market": "KOSPI",
            }
        )

    # Fetch KOSDAQ stocks
    kosdaq_tickers = stock.get_market_ticker_list(market="KOSDAQ")
    for ticker in kosdaq_tickers:
        name = stock.get_market_ticker_name(ticker)
        stocks_to_create.append(
            {
                "name": name,
                "ticker": ticker,
                "market": "KOSDAQ",
            }
        )

    return stocks_to_create


def fetch_daily_prices(
    ticker: str, start_date: str, end_date: str
) -> List[Dict[str, Any]]:
    """
    Fetch daily OHLCV data for a specific ticker from pykrx.

    Args:
        ticker: Stock ticker code (e.g., "005930")
        start_date: Start date in YYYYMMDD format (e.g., "20250101")
        end_date: End date in YYYYMMDD format (e.g., "20251231")

    Returns:
        List of daily price dictionaries ready for bulk creation
    """
    df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)

    daily_prices = []
    for date, row in df.iterrows():
        daily_prices.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "open": float(row["시가"]),
                "high": float(row["고가"]),
                "low": float(row["저가"]),
                "close": float(row["종가"]),
                "volume": int(row["거래량"]),
            }
        )

    return daily_prices
