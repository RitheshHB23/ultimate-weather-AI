#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════
# Ultimate Weather AI - Startup Script (Linux/Mac)
# ═══════════════════════════════════════════════════════════════════════

echo ""
echo "╔═════════════════════════════════════════════════════════════════════╗"
echo "║          🌍 ULTIMATE WEATHER AI - STARTING UP                     ║"
echo "╚═════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found!"
    echo ""
    echo "ℹ️  You need to:"
    echo "   1. Copy .env.example to .env"
    echo "   2. Add your OpenWeatherMap API key to .env"
    echo ""
    echo "📖 See README.md for detailed instructions"
    exit 1
fi

echo "✓ .env file found"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ℹ️  Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo ""
    echo "Trying again with detailed output..."
    pip install -r requirements.txt
    exit 1
fi

echo "✓ Dependencies installed"

echo ""
echo "╔═════════════════════════════════════════════════════════════════════╗"
echo "║          🚀 STARTING FLASK BACKEND                                 ║"
echo "║                                                                     ║"
echo "║  🌐 Frontend:  http://localhost:5000                              ║"
echo "║  📡 API Docs:  http://localhost:5000/api/forecast                 ║"
echo "║                                                                     ║"
echo "║  Press CTRL+C to stop the server                                   ║"
echo "╚═════════════════════════════════════════════════════════════════════╝"
echo ""

python app.py
