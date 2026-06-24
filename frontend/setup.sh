#!/bin/bash

# Cab Booking Frontend Setup Script

echo "Setting up Cab Booking Frontend..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "Creating .env.local file from .env.example..."
    cp .env.example .env.local
    echo "Please edit .env.local file with your configuration"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.local file with your configuration"
echo "2. Run: npm run dev"


