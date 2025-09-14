@echo off
echo Starting Janata Audit System...
echo ==============================

REM Kill any existing processes on our ports
echo Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3001" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1

REM Set environment variables
set NODE_ENV=development
set BACKEND_PORT=3000
set FRONTEND_PORT=3001

REM Check if Python virtual environment exists
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r python_scripts\requirements.txt
) else (
    call .venv\Scripts\activate
)

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install backend dependencies
    goto error
)
cd ..

REM Install frontend dependencies
echo Installing frontend dependencies...
call npm install --legacy-peer-deps
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install frontend dependencies
    goto error
)

REM Create new terminals for each component
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && set PORT=%BACKEND_PORT% && node server.js"

REM Wait for backend to initialize and check if it's running
echo Waiting for backend to start...
timeout /t 5
netstat -ano | find ":%BACKEND_PORT%" | find "LISTENING" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Backend failed to start on port %BACKEND_PORT%
    goto error
)

echo Starting AI Models...
start "Hybrid Health Engine" cmd /k "C:/Users/Jyothika/Desktop/jannat_audit/.venv/Scripts/python.exe python_scripts/hybrid_health_engine/run.py"

REM Wait for AI models to load
timeout /t 3

echo Starting Data Scrapers...
start "Bengaluru Scraper" cmd /k "C:/Users/Jyothika/Desktop/jannat_audit/.venv/Scripts/python.exe python_scripts/bengaluru_project_scraper.py"
start "Government Portal Scraper" cmd /k "C:/Users/Jyothika/Desktop/jannat_audit/.venv/Scripts/python.exe python_scripts/government_portal_scraper.py"

REM Wait for scrapers to initialize
timeout /t 3

echo Starting Frontend Application...
start "Frontend" cmd /k "set PORT=%FRONTEND_PORT% && npm start"

echo.
echo Checking component status...
timeout /t 5

REM Check if frontend started
netstat -ano | find ":%FRONTEND_PORT%" | find "LISTENING" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Frontend might not have started properly on port %FRONTEND_PORT%
) else (
    echo Frontend is running on port %FRONTEND_PORT%
)

REM Check if backend is still running
netstat -ano | find ":%BACKEND_PORT%" | find "LISTENING" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Backend might not be running on port %BACKEND_PORT%
) else (
    echo Backend is running on port %BACKEND_PORT%
)

echo.
echo System Status:
echo -------------
echo Frontend URL: http://localhost:%FRONTEND_PORT%
echo Backend API: http://localhost:%BACKEND_PORT%
echo.
echo To stop all components, run stop_all.bat
echo Press any key to exit this window (other components will keep running)
goto end

:error
echo.
echo Error: System failed to start properly
echo Running cleanup...
call stop_all.bat
exit /b 1

:end
pause > nul