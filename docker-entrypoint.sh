#!/bin/bash
set -e

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload