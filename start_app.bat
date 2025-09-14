@echo off
echo 🚀 Starting Janata Audit Bengaluru
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
echo 📊 Opening http://localhost:8080 in your browser
echo.

REM Start the web server in background
start /B python web_server.py

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:8080

echo ✅ Application started!
echo 🌐 Interface: http://localhost:8080
echo 📝 Press Ctrl+C in the terminal to stop the server
echo.

REM Keep the window open
pause