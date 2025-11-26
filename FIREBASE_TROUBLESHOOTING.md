# Firebase Setup and Troubleshooting Guide

## Current Issue: Missing or Insufficient Permissions

You're seeing this error because Firestore rules haven't been deployed to your Firebase project yet.

## Quick Fix: Deploy Updated Rules

1. **Option 1: Use the Deploy Script**
   ```bash
   # Run this command in the project directory
   ./deploy_firebase_rules.bat
   ```

2. **Option 2: Manual Deployment**
   ```bash
   # Make sure Firebase CLI is installed and you're logged in
   firebase login
   firebase deploy --only firestore:rules
   ```

3. **Option 3: Firebase Console (Web Interface)**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your project: `janta-audit-3c182`
   - Navigate to Firestore Database → Rules
   - Copy the content from `firestore.rules` file
   - Publish the rules

## Current Rules Configuration

The `firestore.rules` file contains comprehensive permissions:

- ✅ **Political Funding Data**: Public read, authenticated write
- ✅ **Audit Reports**: Public read, authenticated write  
- ✅ **System Config**: Public read, admin write
- ✅ **User Interactions**: Authenticated access
- ✅ **Analytics**: Public read, authenticated write
- ✅ **Data Sources**: Public read, authenticated write
- ✅ **Bangalore Projects**: Public read, authenticated write
- ✅ **Social Posts**: Public read, authenticated write/update/delete

## App Functionality Status

**✅ WORKING WITHOUT FIREBASE:**
- Corruption Narrative Synthesizer
- Political funding analysis
- Risk scoring algorithms  
- Forensic investigation reports
- All UI components and visualizations

**⏳ ENHANCED WITH FIREBASE:**
- Real-time data synchronization
- Multi-user collaboration
- Cloud data storage
- Advanced analytics

## If Firebase Deployment Fails

The app is designed to work perfectly without Firebase. All core functionality including the Corruption Narrative Synthesizer operates independently with local sample data.

## Testing the System

1. **Open the app** in your browser
2. **Navigate to Political Funding** section
3. **Click on any donation** to see the investigative analysis
4. **Check the "Corruption Hypothesis" tab** for detailed investigations

The system will show comprehensive corruption analysis even without Firebase connectivity.

## Next Steps

1. Deploy Firebase rules using one of the methods above
2. The app will automatically start using Firebase once rules are deployed
3. No code changes needed - everything is already configured