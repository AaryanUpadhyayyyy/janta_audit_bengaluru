@echo off
echo Stopping Janata Audit System...
echo =============================

REM Kill all running Node.js processes
echo Stopping Node.js processes...
taskkill /F /IM node.exe

REM Kill all running Python processes related to our app
echo Stopping Python processes...
taskkill /F /FI "WINDOWTITLE eq Hybrid Health Engine*"
taskkill /F /FI "WINDOWTITLE eq Bengaluru Scraper*"
taskkill /F /FI "WINDOWTITLE eq Government Portal Scraper*"

REM Kill any remaining cmd windows we started
echo Cleaning up terminal windows...
taskkill /F /FI "WINDOWTITLE eq Backend Server*"
taskkill /F /FI "WINDOWTITLE eq Frontend*"

echo.
echo All components stopped!
echo Press any key to exit
pause > nul