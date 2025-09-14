@echo off
echo 🔥 Starting Janata Audit Bengaluru with Firebase Setup
echo ==================================================

echo.
echo 🚀 Step 1: Setting up Firebase...
python setup_firebase.py

echo.
echo 🚀 Step 2: Starting the application...
python simple_server.py

echo.
echo 🌐 Application started! Open http://localhost:8002 in your browser
echo 📝 Press Ctrl+C to stop the server
pause
