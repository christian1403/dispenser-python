#!/bin/bash

# Flask API Deployment Script

set -e

echo "🚀 Starting Flask API deployment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
pytest

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed! Deployment aborted."
    exit 1
fi

# Create logs directory
mkdir -p logs

# Set production environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

echo "🚦 Starting Flask API in production mode..."

# Start with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log app:app

echo "🎉 Flask API deployed successfully!"
