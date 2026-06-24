#!/bin/bash

# Cab Booking Backend Setup Script

echo "Setting up Cab Booking Backend..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Check if PostgreSQL is running
echo "Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL with PostGIS extension."
else
    echo "PostgreSQL found. Make sure PostGIS extension is enabled:"
    echo "  psql -d cab_booking -c 'CREATE EXTENSION IF NOT EXISTS postgis;'"
fi

# Check if Redis is running
echo "Checking Redis..."
if ! command -v redis-cli &> /dev/null; then
    echo "Redis is not installed. Please install Redis."
else
    echo "Redis found."
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Set up PostgreSQL database with PostGIS"
echo "3. Start Redis server"
echo "4. Run: uvicorn app.main:app --reload"


