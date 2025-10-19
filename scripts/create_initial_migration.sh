#!/bin/bash

# Create initial database migration
echo "Creating initial database migration..."

alembic revision --autogenerate -m "Initial migration: users, articles, comments"

echo "Migration created successfully!"
echo "To apply the migration, run: alembic upgrade head"
