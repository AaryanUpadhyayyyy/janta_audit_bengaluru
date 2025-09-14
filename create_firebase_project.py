#!/usr/bin/env python3
"""
Firebase Project Creation Script for Janata Audit Bengaluru
This script helps create the Firebase project and configure it
"""

import webbrowser
import time
import json
import os

def print_banner():
    print("🔥" + "="*60)
    print("   FIREBASE PROJECT CREATION")
    print("   Janata Audit Bengaluru")
    print("="*62)

def create_firebase_project():
    """Create Firebase project and configure it"""
    print("\n🚀 Creating Firebase Project...")
    print("="*40)
    
    # Open Firebase Console
    print("🌐 Opening Firebase Console...")
    webbrowser.open('https://console.firebase.google.com/')
    
    print("\n📋 FOLLOW THESE STEPS:")
    print("="*25)
    
    steps = [
        "1. Click 'Create a project' in Firebase Console",
        "2. Enter project name: 'janata-audit-bengaluru'",
        "3. Enable Google Analytics (optional)",
        "4. Click 'Create project'",
        "5. Wait for project to be created",
        "6. Click 'Continue' when ready",
        "7. Go to Project Settings (gear icon)",
        "8. Scroll to 'Your apps' section",
        "9. Click Web icon (</>)",
        "10. Enter app nickname: 'janata-audit-web'",
        "11. Click 'Register app'",
        "12. Copy the Firebase configuration",
        "13. Come back here and press Enter"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"   {step}")
        time.sleep(0.3)
    
    input("\n⏳ Press Enter when you've completed the steps above...")

def configure_authentication():
    """Configure Firebase Authentication"""
    print("\n🔐 Configuring Authentication...")
    print("="*35)
    
    print("📋 AUTHENTICATION SETUP:")
    print("="*25)
    
    auth_steps = [
        "1. In Firebase Console, go to 'Authentication'",
        "2. Click 'Get started'",
        "3. Go to 'Sign-in method' tab",
        "4. Enable 'Email/Password' provider",
        "5. Click 'Save'",
        "6. Go to 'Settings' tab",
        "7. Add 'localhost' to Authorized domains",
        "8. Click 'Save'"
    ]
    
    for step in auth_steps:
        print(f"   {step}")
        time.sleep(0.3)
    
    input("\n⏳ Press Enter when authentication is configured...")

def configure_firestore():
    """Configure Firestore Database"""
    print("\n🗄️ Configuring Firestore Database...")
    print("="*40)
    
    print("📋 FIRESTORE SETUP:")
    print("="*20)
    
    firestore_steps = [
        "1. In Firebase Console, go to 'Firestore Database'",
        "2. Click 'Create database'",
        "3. Choose 'Start in test mode'",
        "4. Select location: 'asia-south1' (Mumbai)",
        "5. Click 'Done'",
        "6. Go to 'Rules' tab",
        "7. Replace rules with the provided security rules",
        "8. Click 'Publish'"
    ]
    
    for step in firestore_steps:
        print(f"   {step}")
        time.sleep(0.3)
    
    print("\n🔒 SECURITY RULES:")
    print("="*20)
    
    rules = '''
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Projects are readable by all authenticated users
    match /projects/{projectId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    // Feedback is readable by all authenticated users
    match /feedback/{feedbackId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
    '''
    
    print(rules)
    
    input("\n⏳ Press Enter when Firestore is configured...")

def update_configuration():
    """Update Firebase configuration in the project"""
    print("\n⚙️ Updating Project Configuration...")
    print("="*40)
    
    print("📋 CONFIGURATION UPDATE:")
    print("="*25)
    
    config_steps = [
        "1. Copy the Firebase configuration from the console",
        "2. Update firebase-config.js with your actual keys",
        "3. Update index.html with your actual keys",
        "4. Test the connection",
        "5. Run the migration script"
    ]
    
    for step in config_steps:
        print(f"   {step}")
        time.sleep(0.3)
    
    print("\n💡 Your Firebase configuration should look like this:")
    print("="*55)
    
    sample_config = '''
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "janata-audit-bengaluru.firebaseapp.com",
    projectId: "janata-audit-bengaluru",
    storageBucket: "janata-audit-bengaluru.appspot.com",
    messagingSenderId: "your-actual-sender-id",
    appId: "your-actual-app-id"
};
    '''
    
    print(sample_config)
    
    input("\n⏳ Press Enter when configuration is updated...")

def test_connection():
    """Test Firebase connection"""
    print("\n🧪 Testing Firebase Connection...")
    print("="*35)
    
    print("📋 TESTING STEPS:")
    print("="*18)
    
    test_steps = [
        "1. Start your server: python simple_server.py",
        "2. Open http://localhost:8009 in browser",
        "3. Open browser console (F12)",
        "4. Look for Firebase initialization messages",
        "5. Try signing up with a new email",
        "6. Check if data appears in Firebase Console",
        "7. Submit feedback and check if it's saved"
    ]
    
    for step in test_steps:
        print(f"   {step}")
        time.sleep(0.3)
    
    print("\n✅ SUCCESS INDICATORS:")
    print("="*22)
    print("   - Firebase initialization messages in console")
    print("   - User registration works")
    print("   - Data appears in Firebase Console")
    print("   - Feedback submission works")
    print("   - Real-time updates work")

def main():
    print_banner()
    
    print("\n🎯 This script will help you create and configure Firebase for your project.")
    print("   Make sure you have a Google account and access to Firebase Console.")
    
    input("\n⏳ Press Enter to start...")
    
    # Step 1: Create Firebase project
    create_firebase_project()
    
    # Step 2: Configure Authentication
    configure_authentication()
    
    # Step 3: Configure Firestore
    configure_firestore()
    
    # Step 4: Update configuration
    update_configuration()
    
    # Step 5: Test connection
    test_connection()
    
    print("\n🎉 FIREBASE SETUP COMPLETE!")
    print("="*30)
    print("Your project is now connected to Firebase!")
    print("Login info and feedback will be saved to the database.")
    print("\n🚀 Next steps:")
    print("   1. Start your server: python simple_server.py")
    print("   2. Open http://localhost:8009")
    print("   3. Test the login and feedback features")
    print("   4. Check Firebase Console to see your data")

if __name__ == "__main__":
    main()
