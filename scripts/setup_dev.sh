#!/bin/bash

# Development environment setup script

echo "Setting up development environment..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

echo "Setup complete!"
echo "To start the development server, run: uvicorn app.main:app --reload"
