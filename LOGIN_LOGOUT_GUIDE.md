# 🔐 Login/Logout Guide - Janata Audit Bengaluru

## 📍 **Where to Find Login/Logout:**

### **1. Dedicated Pages:**
- **Login Page:** `login.html` - Full-featured login/signup page
- **Logout Page:** `logout.html` - Dedicated logout confirmation page

### **2. Integrated in Navigation:**
- **All Pages** have login/logout buttons in the top navigation bar
- **Sign In/Sign Up** buttons appear when user is not logged in
- **User Menu** appears when user is logged in (shows name, role, and logout button)

## 🚀 **How to Access Login/Logout:**

### **Method 1: Direct URLs**
```
Login: http://localhost:8002/login.html
Logout: http://localhost:8002/logout.html
```

### **Method 2: Navigation Buttons**
- Click **"Sign In"** or **"Sign Up"** in the top navigation
- Click **"Sign Out"** in the user menu (when logged in)

### **Method 3: Programmatic Access**
```javascript
// Show login modal (on any page)
authSystem.showSignIn();

// Show signup modal (on any page)
authSystem.showSignUp();

// Sign out user
authSystem.signOut();
```

## 🎨 **Login Page Features:**

### **Located at:** `login.html`

#### **Features:**
- ✅ **Beautiful UI** with gradient background
- ✅ **Tab-based interface** (Sign In / Sign Up)
- ✅ **Form validation** and error handling
- ✅ **Demo credentials** displayed for testing
- ✅ **Auto-redirect** to dashboard after successful login
- ✅ **Responsive design** for mobile and desktop

#### **Demo Credentials:**
- **Email:** admin@janataaudit.com
- **Password:** admin123

## 🚪 **Logout Page Features:**

### **Located at:** `logout.html`

#### **Features:**
- ✅ **Confirmation message** with user info
- ✅ **Auto-logout** after 2 seconds
- ✅ **Loading animation** during logout process
- ✅ **Navigation options** (Sign In Again / Back to Home)
- ✅ **User information** display before logout

## 🔄 **Authentication Flow:**

### **Login Process:**
1. User clicks **"Sign In"** or visits `/login.html`
2. User enters credentials
3. System validates with Firebase (or mock auth)
4. User is redirected to dashboard
5. Navigation updates to show user menu

### **Logout Process:**
1. User clicks **"Sign Out"** in navigation
2. User is redirected to `/logout.html`
3. System clears user session
4. User sees confirmation message
5. User can sign in again or go home

## 📱 **Navigation Integration:**

### **When NOT Logged In:**
```html
<div id="authButtons">
    <a href="login.html" class="btn btn-secondary">Sign In</a>
    <a href="login.html" class="btn btn-primary">Sign Up</a>
</div>
```

### **When Logged In:**
```html
<div id="userMenu">
    <div class="user-info">
        <span class="user-name">John Doe</span>
        <span class="user-role">citizen</span>
    </div>
    <div class="user-actions">
        <a href="logout.html" class="btn btn-secondary">Sign Out</a>
    </div>
</div>
```

## 🛠️ **Technical Implementation:**

### **Files Involved:**
- `login.html` - Dedicated login page
- `logout.html` - Dedicated logout page
- `auth-system.js` - Authentication logic
- `firebase-config.js` - Firebase integration
- All page navigation bars

### **Authentication States:**
1. **Not Authenticated** - Shows Sign In/Sign Up buttons
2. **Authenticated** - Shows user menu with logout option
3. **Logging Out** - Shows loading state and confirmation

## 🎯 **Quick Start:**

### **To Test Login/Logout:**
1. **Start the server:** `python simple_server.py`
2. **Open:** `http://localhost:8002`
3. **Click:** "Sign In" in navigation
4. **Use demo credentials:** admin@janataaudit.com / admin123
5. **Test logout:** Click "Sign Out" in user menu

### **To Access Directly:**
- **Login:** `http://localhost:8002/login.html`
- **Logout:** `http://localhost:8002/logout.html`

## 🔧 **Customization:**

### **Change Login Page:**
- Edit `login.html` for UI changes
- Modify `auth-system.js` for logic changes

### **Change Logout Page:**
- Edit `logout.html` for UI changes
- Modify logout behavior in `auth-system.js`

### **Add to New Pages:**
- Include the navigation HTML
- Include `auth-system.js` script
- The authentication will work automatically

## 📊 **Current Status:**

✅ **Login page created** - `login.html`
✅ **Logout page created** - `logout.html`
✅ **Navigation integrated** - All pages
✅ **Authentication working** - Mock and Firebase ready
✅ **User experience** - Smooth and professional

## 🚀 **Ready to Use!**

Your login/logout system is fully functional and ready to use! Users can:
- Sign in with demo credentials
- Create new accounts
- Access all features when logged in
- Sign out securely
- Navigate between pages seamlessly

**Start testing at:** `http://localhost:8002/login.html` 🎉
