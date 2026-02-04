#!/bin/bash

echo "Starting Telegram Music Bot..."
echo "================================"

if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/Updating dependencies..."
pip install -r requirements.txt

echo "Creating cache directories..."
mkdir -p cache/music cache/voice

echo "Starting bot..."
python bot.py
