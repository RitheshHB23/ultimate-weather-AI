@echo off
REM ═══════════════════════════════════════════════════════════════════════
REM  Ultimate Weather AI - Startup Script (Windows)
REM ═══════════════════════════════════════════════════════════════════════

echo.
echo ╔═════════════════════════════════════════════════════════════════════╗
echo ║          🌍 ULTIMATE WEATHER AI - STARTING UP                     ║
echo ╚═════════════════════════════════════════════════════════════════════╝
echo.

REM Check if .env file exists
if not exist .env (
    echo ❌ ERROR: .env file not found!
    echo.
    echo ℹ️  You need to:
    echo    1. Copy .env.example to .env
    echo    2. Add your OpenWeatherMap API key to .env
    echo.
    echo 📖 See README.md for detailed instructions
    pause
    exit /b 1
)

echo ✓ .env file found
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ℹ️  Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install dependencies
    echo.
    echo Trying again with detailed output...
    pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo ╔═════════════════════════════════════════════════════════════════════╗
echo ║          🚀 STARTING FLASK BACKEND                                 ║
echo ║                                                                     ║
echo ║  🌐 Frontend:  http://localhost:5000                              ║
echo ║  📡 API Docs:  http://localhost:5000/api/forecast                 ║
echo ║                                                                     ║
echo ║  Press CTRL+C to stop the server                                   ║
echo ╚═════════════════════════════════════════════════════════════════════╝
echo.

python app.py
