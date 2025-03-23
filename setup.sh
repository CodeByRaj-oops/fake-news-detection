#!/bin/bash
# Setup script for Fake News Detection project

echo "Installing root dependencies..."
npm install

echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Installing backend dependencies..."
cd backend
npm install
cd ..

echo "Installing Python dependencies..."
cd backend
# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate || source .venv/Scripts/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

echo "Setup complete! Run 'npm run dev' to start the application." 