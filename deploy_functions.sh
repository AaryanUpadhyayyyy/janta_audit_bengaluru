#!/bin/bash

echo "Deploying Firebase Cloud Functions..."
echo

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "Error: Firebase CLI is not installed or not in PATH"
    echo "Please install Firebase CLI: npm install -g firebase-tools"
    exit 1
fi

# Check if user is logged in
if ! firebase projects:list &> /dev/null; then
    echo "You need to login to Firebase first"
    echo "Running: firebase login"
    firebase login
fi

# Navigate to functions directory and install dependencies
cd functions
echo "Installing function dependencies..."
npm install

# Return to root directory
cd ..

# Deploy functions
echo
echo "Deploying Cloud Functions..."
firebase deploy --only functions

if [ $? -eq 0 ]; then
    echo
    echo "✅ Firebase Cloud Functions deployed successfully!"
    echo
    echo "Available functions:"
    echo "- updateFollowStatus: Main follow/unfollow functionality"
    echo "- getUserFollowStats: Get user follower statistics"
    echo "- checkFollowStatus: Check if user A follows user B"
    echo "- onUserCreate: Auto-initialize new user follow counts"
    echo "- syncFollowerCounts: Daily data consistency check"
    echo
else
    echo
    echo "❌ Deployment failed. Please check the error messages above."
    echo
fi