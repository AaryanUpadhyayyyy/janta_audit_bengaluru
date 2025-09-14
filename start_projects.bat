@echo off
echo 🚀 Starting Janata Audit Bengaluru Projects System
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
echo 🌐 Starting Web Server...
echo 📊 Open http://localhost:8080 in your browser to view the interface
echo 🗺️ API available at: http://localhost:8080/api/projects
echo.

REM Start the web server
python web_server.py

pause
