import time
from app.worker import celery_app # Import the Celery app

# This is your background task for stocks
@celery_app.task
def run_stock_pipeline():
    """
    This is your long-running task.
    1. Gather stock data from outer API
    2. Loop creating of retrieved data
    3. Same thing for price
    """
    print("Stock pipeline started...")
    time.sleep(10)
    print("...Stock pipeline finished!")
    
    return "Stock and price data successfully imported."

# You can add other stock-related tasks here
# @celery_app.task
# def update_single_stock_price(stock_id):
#     ...