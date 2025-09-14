#!/usr/bin/env python3
"""
Firebase Setup Helper for Janata Audit Bengaluru
This script helps you set up Firebase and migrate your data
"""

import json
import os
import webbrowser
import time

def print_banner():
    print("🔥" + "="*50)
    print("   FIREBASE SETUP HELPER")
    print("   Janata Audit Bengaluru")
    print("="*52)

def check_firebase_config():
    """Check if Firebase configuration is set up"""
    print("\n🔍 Checking Firebase configuration...")
    
    # Check if firebase-config.js exists
    if os.path.exists('firebase-config.js'):
        with open('firebase-config.js', 'r') as f:
            content = f.read()
            
        if 'your-api-key-here' in content:
            print("❌ Firebase configuration not set up yet")
            print("💡 Please update firebase-config.js with your actual Firebase credentials")
            return False
        else:
            print("✅ Firebase configuration appears to be set up")
            return True
    else:
        print("❌ firebase-config.js not found")
        return False

def open_firebase_console():
    """Open Firebase Console in browser"""
    print("\n🌐 Opening Firebase Console...")
    webbrowser.open('https://console.firebase.google.com/')
    print("✅ Firebase Console opened in your browser")

def show_setup_steps():
    """Show step-by-step setup instructions"""
    print("\n📋 FIREBASE SETUP STEPS:")
    print("="*30)
    
    steps = [
        "1. Go to Firebase Console (opened in browser)",
        "2. Click 'Create a project'",
        "3. Enter project name: 'janata-audit-bengaluru'",
        "4. Enable Google Analytics (optional)",
        "5. Go to Project Settings > General > Your apps",
        "6. Click Web icon and register your app",
        "7. Copy the Firebase configuration",
        "8. Update firebase-config.js with your credentials",
        "9. Enable Authentication (Email/Password)",
        "10. Create Firestore Database",
        "11. Run this script again to migrate data"
    ]
    
    for step in steps:
        print(f"   {step}")
        time.sleep(0.5)

def migrate_data():
    """Migrate existing data to Firebase"""
    print("\n🚀 Starting data migration...")
    
    # Check if projects data exists
    if os.path.exists('bengaluru_projects.json'):
        print("✅ Found existing projects data")
        
        with open('bengaluru_projects.json', 'r') as f:
            projects_data = json.load(f)
            
        print(f"📊 Found {len(projects_data.get('projects', []))} projects")
        print("💡 Open your browser and run: new DatabaseMigration().runMigration()")
    else:
        print("❌ No existing projects data found")
        print("💡 Run the scraper first to generate project data")

def show_firebase_rules():
    """Show Firestore security rules"""
    print("\n🔒 FIRESTORE SECURITY RULES:")
    print("="*35)
    
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
    print("💡 Copy these rules to Firebase Console > Firestore Database > Rules")

def main():
    print_banner()
    
    # Check current status
    firebase_configured = check_firebase_config()
    
    if not firebase_configured:
        print("\n🚀 Let's set up Firebase!")
        open_firebase_console()
        show_setup_steps()
        show_firebase_rules()
    else:
        print("\n✅ Firebase appears to be configured!")
        migrate_data()
    
    print("\n🎯 NEXT STEPS:")
    print("="*15)
    print("1. Complete Firebase setup in the browser")
    print("2. Update firebase-config.js with your credentials")
    print("3. Start your server: python simple_server.py")
    print("4. Open http://localhost:8002")
    print("5. Open browser console and run: new DatabaseMigration().runMigration()")
    print("6. Test the system with Firebase!")
    
    print("\n🔥 Firebase setup complete! Happy coding!")

if __name__ == "__main__":
    main()
