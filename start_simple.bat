@echo off
echo 🚀 Starting Janata Audit Bengaluru (Simple Version)
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Install required packages
echo 📦 Installing required packages...
pip install requests beautifulsoup4 selenium webdriver-manager lxml pandas

echo.
echo 🌐 Starting Simple Web Server...
echo 📊 This will automatically find a free port and open your browser
echo.

REM Start the simple server
python simple_server.py

pause
