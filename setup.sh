#!/bin/bash

echo "Telegram Music Bot Setup"
echo "========================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $PYTHON_VERSION"

if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg is not installed!"
    echo "Installing FFmpeg..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg portaudio19-dev
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg portaudio
    else
        echo "Please install FFmpeg manually"
    fi
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p cache/music cache/voice

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env file and add your credentials:"
    echo "  - API_ID and API_HASH from https://my.telegram.org"
    echo "  - BOT_TOKEN from @BotFather"
    echo "  - STRING_SESSION (run: python generate_session.py)"
    echo "  - LOGGER_GROUP_ID (your logger group ID)"
    echo "  - MONGODB_URI (your MongoDB connection string)"
    echo "  - OWNER_ID (your Telegram user ID)"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Generate string session: python generate_session.py"
echo "2. Edit .env file with your credentials"
echo "3. Run the bot: ./start.sh or python bot.py"
echo ""
