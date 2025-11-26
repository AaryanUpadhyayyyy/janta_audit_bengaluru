# Firebase Authentication Setup Guide for Jannat Audit

## 🔐 Enable Authentication Providers

To fix the authentication issue, you need to enable sign-in providers in Firebase Console:

### Step 1: Go to Firebase Console
1. Open: https://console.firebase.google.com/project/janta-audit-3c182
2. Click on "Authentication" in the left sidebar
3. Click on "Sign-in method" tab

### Step 2: Enable Google Sign-In
1. Click on "Google" provider
2. Click "Enable" toggle switch
3. Add your project support email: aaryanpandit20032006@gmail.com
4. Click "Save"

### Step 3: Enable Anonymous Sign-In (Fallback)
1. Click on "Anonymous" provider
2. Click "Enable" toggle switch
3. Click "Save"

### Step 4: Optional - Enable Email/Password
1. Click on "Email/Password" provider
2. Click "Enable" toggle switch for "Email/Password"
3. Click "Save"

## 🌐 Add Authorized Domains
1. Go to "Settings" tab in Authentication
2. In "Authorized domains" section, add:
   - localhost (should already be there)
   - janta-audit-3c182.web.app (for future hosting)
   - Your custom domain if you have one

## 🎯 After Setup
Once you enable these providers:
1. Refresh your Jannat Audit application
2. Click the "🔑 Sign In" button
3. Choose Google sign-in when prompted
4. You should see your email appear in the "Users" tab

## 🔧 Troubleshooting
If Google sign-in doesn't work:
- The app will automatically try anonymous sign-in as fallback
- Check browser console for any error messages
- Make sure popup blockers are disabled

## ✅ Expected Result
After setup, you should see:
- Your email in Firebase Console > Authentication > Users
- "👤 your-email@gmail.com" in the app's authentication section
- Ability to sign in/out using the button