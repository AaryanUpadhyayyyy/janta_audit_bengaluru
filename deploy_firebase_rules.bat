@echo off
echo 🚀 Deploying Firebase Firestore Rules...
echo.
echo This will deploy the updated firestore.rules to your Firebase project.
echo Make sure you're logged in to Firebase CLI.
echo.
pause
echo.
echo Deploying rules...
firebase deploy --only firestore:rules
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Firebase rules deployed successfully!
    echo.
    echo The updated rules now allow:
    echo - Public read access for transparency data
    echo - Authenticated write access for security
    echo - Proper permissions for all collections
    echo.
) else (
    echo ❌ Failed to deploy Firebase rules
    echo Please check your Firebase CLI setup and try again
    echo.
)
pause