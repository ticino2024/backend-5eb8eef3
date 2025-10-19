#!/bin/bash

echo "========================================"
echo "Running Blog Platform API Tests"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "Running pytest..."
echo ""

pytest -v --tb=short

echo ""
echo "========================================"
echo "Test run complete!"
echo "========================================"
