# 🔥 Complete Firebase Database Setup Guide

## 🚀 **Step 1: Create Firebase Project**

### **1.1 Go to Firebase Console**
- Visit: https://console.firebase.google.com/
- Click **"Create a project"**
- Enter project name: `janata-audit-bengaluru`
- Enable Google Analytics (optional)
- Click **"Create project"**

### **1.2 Get Project Configuration**
- Go to **Project Settings** (gear icon)
- Scroll to **"Your apps"** section
- Click **"Web"** icon (`</>`)
- Enter app nickname: `janata-audit-web`
- Click **"Register app"**
- **Copy the Firebase configuration object**

## 🔐 **Step 2: Enable Authentication**

### **2.1 Set up Authentication**
- In Firebase Console, go to **"Authentication"**
- Click **"Get started"**
- Go to **"Sign-in method"** tab
- Enable **"Email/Password"** provider
- Click **"Save"**

### **2.2 Configure Authentication Settings**
- Go to **"Authentication" > "Settings"**
- Add your domain to **"Authorized domains"**
- Add `localhost` for development

## 🗄️ **Step 3: Set up Firestore Database**

### **3.1 Create Database**
- Go to **"Firestore Database"**
- Click **"Create database"**
- Choose **"Start in test mode"** (for development)
- Select location: **"asia-south1"** (Mumbai - closest to India)
- Click **"Done"**

### **3.2 Configure Security Rules**
Go to **"Firestore Database" > "Rules"** and replace with:

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
    
    // Reports are readable by all authenticated users
    match /reports/{reportId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

## 📝 **Step 4: Update Your Configuration**

### **4.1 Replace Firebase Config**
In `index.html`, replace the placeholder configuration:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-actual-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "your-actual-sender-id",
    appId: "your-actual-app-id"
};
```

### **4.2 Test Connection**
- Open browser console
- Look for Firebase connection messages
- Try signing up with a new email
- Check if data appears in Firebase Console

## 🗂️ **Step 5: Database Collections Structure**

### **5.1 Users Collection**
```
users/
├── {userId}/
    ├── uid: string
    ├── email: string
    ├── name: string
    ├── role: string (citizen/admin)
    ├── createdAt: timestamp
    └── updatedAt: timestamp
```

### **5.2 Projects Collection**
```
projects/
├── {projectId}/
    ├── projectName: string
    ├── description: string
    ├── budget: number
    ├── status: string
    ├── department: string
    ├── location: string
    ├── wardNumber: string
    ├── startDate: timestamp
    ├── endDate: timestamp
    ├── geoPoint: object
    ├── createdAt: timestamp
    └── updatedAt: timestamp
```

### **5.3 Feedback Collection**
```
feedback/
├── {feedbackId}/
    ├── projectId: string
    ├── projectName: string
    ├── user: string
    ├── email: string
    ├── category: string
    ├── rating: number
    ├── comment: string
    ├── location: string
    ├── status: string
    └── createdAt: timestamp
```

## 🔄 **Step 6: Data Migration**

### **6.1 Migrate Existing Projects**
Run this script to migrate your existing projects to Firebase:

```javascript
// Run in browser console after Firebase setup
async function migrateProjects() {
    const response = await fetch('/api/projects');
    const data = await response.json();
    
    for (const project of data.projects) {
        const result = await addProject(project);
        console.log(`Migrated project: ${project.projectName}`, result);
    }
}
```

### **6.2 Test Data Operations**
- Create new user account
- Submit feedback
- Check data in Firebase Console
- Verify real-time updates

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"Firebase auth failed"**
   - Check API keys are correct
   - Verify project ID matches
   - Check if authentication is enabled

2. **"Permission denied"**
   - Check Firestore security rules
   - Verify user is authenticated
   - Check collection names match

3. **"Network error"**
   - Check internet connection
   - Verify Firebase project is active
   - Check browser console for errors

### **Debug Mode:**
```javascript
// Add to browser console for debugging
console.log('Firebase Auth:', window.firebaseAuth);
console.log('Firebase DB:', window.firebaseDb);
```

## ✅ **Verification Checklist**

- [ ] Firebase project created
- [ ] Authentication enabled
- [ ] Firestore database created
- [ ] Security rules configured
- [ ] Configuration updated in code
- [ ] Test user registration works
- [ ] Test feedback submission works
- [ ] Data appears in Firebase Console
- [ ] Real-time updates working

## 🎯 **Next Steps After Setup**

1. **Real-time updates** for project data
2. **User role management** with Firestore
3. **Push notifications** for project updates
4. **Advanced analytics** with Firebase Analytics
5. **File storage** for project documents

## 📞 **Support**

If you encounter issues:
1. Check browser console for error messages
2. Verify Firebase project configuration
3. Test with a simple Firebase app first
4. Check Firebase documentation: https://firebase.google.com/docs

---

**Your system will work with Firebase once you complete these steps!** 🚀
