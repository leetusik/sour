# sour

[] routinable stock price gathering
    post /api/v1/stocks
    post /api/v1/stocks/{stock_id}/daily_prices
    
    delete /api/v1/stocks/{stock_id}
    delete /api/v1/stocks/{stock_id}/daily_prices/{daily_price_id}

    - every day just gather all stocks again because of adjusted price

[] routinable stock financial statements gathering
    post /api/v1/stocks/{stock_id}/financial_statements

    - first time gather the FS over years
    - after that, every day check if there is a new FS.

---
## commands
```bash
# make migrations
docker compose exec sour-app alembic revision --autogenerate -m "Your migration message"

# migrate(using docker-entrypoint.sh)
docker compose restart sour-app
```