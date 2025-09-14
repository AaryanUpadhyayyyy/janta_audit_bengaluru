@echo off
REM Janata Audit Bengaluru - Deployment Script for Windows

echo 🚀 Starting deployment of Janata Audit Bengaluru...

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found. Please install it first:
    echo npm install -g firebase-tools
    pause
    exit /b 1
)

REM Check if user is logged in to Firebase
firebase projects:list >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Please login to Firebase first:
    echo firebase login
    pause
    exit /b 1
)

REM Build React app
echo 📦 Building React application...
call npm run build

if %errorlevel% neq 0 (
    echo ❌ Build failed. Please check for errors.
    pause
    exit /b 1
)

REM Deploy Firebase functions
echo 🔧 Deploying Firebase functions...
cd functions
call npm install
cd ..

firebase deploy --only functions

if %errorlevel% neq 0 (
    echo ❌ Functions deployment failed.
    pause
    exit /b 1
)

REM Deploy Firestore rules
echo 📋 Deploying Firestore rules...
firebase deploy --only firestore:rules

if %errorlevel% neq 0 (
    echo ❌ Firestore rules deployment failed.
    pause
    exit /b 1
)

REM Deploy Firestore indexes
echo 📊 Deploying Firestore indexes...
firebase deploy --only firestore:indexes

if %errorlevel% neq 0 (
    echo ❌ Firestore indexes deployment failed.
    pause
    exit /b 1
)

REM Deploy hosting
echo 🌐 Deploying to Firebase Hosting...
firebase deploy --only hosting

if %errorlevel% neq 0 (
    echo ❌ Hosting deployment failed.
    pause
    exit /b 1
)

echo ✅ Deployment completed successfully!
echo 🎉 Janata Audit Bengaluru is now live!

echo.
echo 📱 Application URLs:
firebase hosting:channel:list

echo.
echo 🔧 Next steps:
echo 1. Set up your environment variables in Firebase Functions
echo 2. Configure your Google Maps API key
echo 3. Run the Python data scraping scripts
echo 4. Train the ML model for delay prediction
echo.
echo 📚 For more information, check the README.md file

pause
