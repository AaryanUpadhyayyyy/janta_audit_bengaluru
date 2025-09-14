@echo off
echo 🚀 Starting Janata Audit Bengaluru Launcher
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

REM Start the launcher server
echo 🌐 Starting launcher server...
echo 📝 Open http://localhost:8080 in your browser
echo.

python launcher_server.py

pause
