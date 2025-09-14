# 🔥 Firebase Quick Setup Guide

## 🚀 **Step 1: Create Firebase Project**

1. **Go to:** https://console.firebase.google.com/
2. **Click:** "Create a project"
3. **Enter name:** `janata-audit-bengaluru`
4. **Enable Google Analytics:** (optional)
5. **Click:** "Create project"

## 🔐 **Step 2: Enable Authentication**

1. **Go to:** Authentication → Get started
2. **Click:** "Sign-in method" tab
3. **Enable:** "Email/Password" provider
4. **Click:** "Save"

## 🗄️ **Step 3: Create Firestore Database**

1. **Go to:** Firestore Database → Create database
2. **Choose:** "Start in test mode"
3. **Select location:** "asia-south1" (Mumbai)
4. **Click:** "Done"

## ⚙️ **Step 4: Get Configuration**

1. **Go to:** Project Settings (gear icon)
2. **Scroll to:** "Your apps" section
3. **Click:** Web icon (`</>`)
4. **Enter nickname:** `janata-audit-web`
5. **Click:** "Register app"
6. **Copy the configuration**

## 🔒 **Step 5: Set Security Rules**

Go to **Firestore Database → Rules** and paste:

```javascript
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
```

## 📝 **Step 6: Update Configuration**

Replace the configuration in `index.html` and `firebase-config.js` with your actual Firebase config:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "janata-audit-bengaluru.firebaseapp.com",
    projectId: "janata-audit-bengaluru",
    storageBucket: "janata-audit-bengaluru.appspot.com",
    messagingSenderId: "your-actual-sender-id",
    appId: "your-actual-app-id"
};
```

## 🧪 **Step 7: Test Connection**

1. **Start server:** `python simple_server.py`
2. **Open:** http://localhost:8009/test_firebase_connection.html
3. **Click:** "Test Firebase Connection"
4. **Check:** Console for success messages

## ✅ **Step 8: Test Features**

1. **Go to:** http://localhost:8009/login.html
2. **Sign up** with a new email
3. **Submit feedback** on any project
4. **Check Firebase Console** to see your data

## 🎉 **Success!**

Your project is now connected to Firebase! All login info and feedback will be saved to the database.

---

**Need help?** Check the browser console for error messages or run the test page to diagnose issues.