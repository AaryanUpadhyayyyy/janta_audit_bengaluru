@echo off
echo Deploying Firebase Cloud Functions...
echo.

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Firebase CLI is not installed or not in PATH
    echo Please install Firebase CLI: npm install -g firebase-tools
    pause
    exit /b 1
)

REM Check if user is logged in
firebase projects:list >nul 2>&1
if %errorlevel% neq 0 (
    echo You need to login to Firebase first
    echo Running: firebase login
    firebase login
)

REM Navigate to functions directory and install dependencies
cd functions
echo Installing function dependencies...
npm install

REM Return to root directory
cd ..

REM Deploy functions
echo.
echo Deploying Cloud Functions...
firebase deploy --only functions

if %errorlevel% equ 0 (
    echo.
    echo ✅ Firebase Cloud Functions deployed successfully!
    echo.
    echo Available functions:
    echo - updateFollowStatus: Main follow/unfollow functionality
    echo - getUserFollowStats: Get user follower statistics
    echo - checkFollowStatus: Check if user A follows user B
    echo - onUserCreate: Auto-initialize new user follow counts
    echo - syncFollowerCounts: Daily data consistency check
    echo.
) else (
    echo.
    echo ❌ Deployment failed. Please check the error messages above.
    echo.
)

pause