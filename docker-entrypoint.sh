#!/bin/bash
set -e

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application (whatever command is passed)
echo "Starting application..."
exec "$@"