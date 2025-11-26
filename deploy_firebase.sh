# Firebase Deployment Script for Jannat Audit
# This script helps deploy the Firestore security rules to your Firebase project

echo "🚀 Deploying Jannat Audit to Firebase..."
echo "📁 Project ID: janta-audit-3c182"

# Make sure you have Firebase CLI installed
# npm install -g firebase-tools

# Login to Firebase (if not already logged in)
echo "🔐 Checking Firebase authentication..."
firebase login

# Initialize Firebase project (if not already done)
echo "🏗️ Initializing Firebase project..."
firebase init firestore --project janta-audit-3c182

# Deploy Firestore rules
echo "📋 Deploying Firestore security rules..."
firebase deploy --only firestore:rules --project janta-audit-3c182

# Deploy Firestore indexes (if any)
echo "📊 Deploying Firestore indexes..."
firebase deploy --only firestore:indexes --project janta-audit-3c182

echo "✅ Firebase deployment complete!"
echo ""
echo "🔗 Your Firebase Console: https://console.firebase.google.com/project/janta-audit-3c182"
echo "🌐 Your app URL: https://janta-audit-3c182.web.app"
echo ""
echo "📋 Next steps:"
echo "1. Open the Firebase Console to verify deployment"
echo "2. Test the application with live Firebase data"
echo "3. Monitor usage in Firebase Analytics"