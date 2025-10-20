#!/bin/bash
set -e

echo "Starting database initialization..."

# Check if migrations exist
if [ -z "$(ls -A /app/alembic/versions/*.py 2>/dev/null)" ]; then
    echo "No migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

