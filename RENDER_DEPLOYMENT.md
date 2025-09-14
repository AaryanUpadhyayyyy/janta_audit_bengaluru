# 🚀 Render Deployment Guide

This guide will help you deploy the Janata Audit backend to Render for **FREE** without requiring billing setup.

## 📋 Prerequisites

1. **GitHub Account** - Free
2. **Render Account** - Free (sign up with GitHub)
3. **Firebase Project** - Free tier
4. **Code pushed to GitHub** - Your project repository

## 🔧 Step 1: Prepare Your Code

### 1.1 Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit with Express.js backend for Render"

# Add remote origin (replace with your GitHub repository URL)
git remote add origin https://github.com/your-username/janata-audit-bengaluru.git

# Push to GitHub
git push -u origin main
```

### 1.2 Verify Backend Structure

Make sure your repository has this structure:
```
janata-audit-bengaluru/
├── backend/
│   ├── server.js
│   ├── package.json
│   └── env.example
├── src/
├── public/
├── package.json
└── render.yaml
```

## 🌐 Step 2: Deploy to Render

### 2.1 Create Render Account

1. **Go to [render.com](https://render.com)**
2. **Click "Get Started for Free"**
3. **Sign up with GitHub** (recommended)
4. **Verify your email**

### 2.2 Create New Web Service

1. **Click "New +"** in Render dashboard
2. **Select "Web Service"**
3. **Connect your GitHub repository**

### 2.3 Configure Service Settings

```
┌─────────────────────────────────────────────────────────┐
│  Create Web Service                                     │
├─────────────────────────────────────────────────────────┤
│  Repository: your-username/janata-audit-bengaluru      │
│  Branch: main                                           │
│  Root Directory: backend                               │
│  Environment: Node                                      │
│  Plan: Free                                            │
│                                                         │
│  Build Command: npm install                            │
│  Start Command: npm start                              │
│                                                         │
│  [Create Web Service]                                   │
└─────────────────────────────────────────────────────────┘
```

**Important Settings:**
- **Root Directory**: `backend`
- **Plan**: `Free`
- **Build Command**: `npm install`
- **Start Command**: `npm start`

### 2.4 Set Environment Variables

In the Render dashboard, go to **Environment** tab:

```
┌─────────────────────────────────────────────────────────┐
│  Environment Variables                                  │
├─────────────────────────────────────────────────────────┤
│  NODE_ENV = production                                  │
│  FIREBASE_SERVICE_ACCOUNT_KEY = [Your service key JSON] │
│  FIREBASE_DATABASE_URL = https://your-project.firebaseio.com │
└─────────────────────────────────────────────────────────┘
```

**How to get Firebase Service Account Key:**

1. **Go to Firebase Console** → **Project Settings** → **Service Accounts**
2. **Click "Generate new private key"**
3. **Download the JSON file**
4. **Copy the entire JSON content** and paste it as `FIREBASE_SERVICE_ACCOUNT_KEY`

### 2.5 Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (2-3 minutes)
3. **Get your API URL** (e.g., `https://janata-audit-backend.onrender.com`)

## 🔗 Step 3: Update Frontend Configuration

### 3.1 Update Environment Variables

Create `.env` file in your project root:

```bash
# Firebase Configuration
REACT_APP_FIREBASE_API_KEY=your_api_key_here
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id

# API Configuration
REACT_APP_API_URL=https://janata-audit-backend.onrender.com/api

# Google Maps API Key
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### 3.2 Test the API

```bash
# Test health endpoint
curl https://janata-audit-backend.onrender.com/api/health

# Expected response:
{
  "status": "OK",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "environment": "production",
  "firebase": true
}
```

## 🎯 Step 4: Deploy Frontend (Optional)

### 4.1 Deploy to Netlify (Free)

1. **Go to [netlify.com](https://netlify.com)**
2. **Sign up with GitHub**
3. **Connect your repository**
4. **Set build settings:**
   - **Build command**: `npm run build`
   - **Publish directory**: `build`
5. **Deploy**

### 4.2 Deploy to Vercel (Free)

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up with GitHub**
3. **Import your repository**
4. **Deploy**

## 🔍 Step 5: Verify Deployment

### 5.1 Test API Endpoints

```bash
# Health check
curl https://your-backend-url.onrender.com/api/health

# Submit feedback
curl -X POST https://your-backend-url.onrender.com/api/submit-feedback \
  -H "Content-Type: application/json" \
  -d '{"projectId":"test","feedback":"Great project!","rating":5}'

# Get projects
curl https://your-backend-url.onrender.com/api/projects
```

### 5.2 Check Logs

In Render dashboard:
1. **Go to your service**
2. **Click "Logs" tab**
3. **Check for any errors**

## 🚨 Troubleshooting

### Common Issues

#### Issue 1: "Database not initialized"
**Solution**: Check Firebase service account key format
```bash
# Make sure the JSON is properly formatted
echo $FIREBASE_SERVICE_ACCOUNT_KEY | jq .
```

#### Issue 2: "Module not found"
**Solution**: Check package.json dependencies
```bash
# In backend directory
npm install
```

#### Issue 3: "Port already in use"
**Solution**: Render handles this automatically, but check your start command
```json
{
  "scripts": {
    "start": "node server.js"
  }
}
```

#### Issue 4: "CORS errors"
**Solution**: CORS is already configured in server.js

### Debug Commands

```bash
# Check if service is running
curl -I https://your-backend-url.onrender.com/api/health

# Check logs in Render dashboard
# Go to your service → Logs tab

# Test locally
cd backend
npm install
npm start
```

## 📊 Monitoring

### Render Dashboard Features

1. **Metrics**: CPU, Memory, Response time
2. **Logs**: Real-time application logs
3. **Deployments**: Deployment history
4. **Environment**: Environment variables

### Free Tier Limits

- **750 hours/month** (31 days × 24 hours = 744 hours) - **UNLIMITED for our project!**
- **512MB RAM** - Sufficient for Express.js
- **Automatic deployments** from GitHub
- **Custom domains** (free)

## 🎉 Success!

Your backend is now deployed on Render for **FREE**! 

**Next Steps:**
1. **Update your frontend** to use the new API URL
2. **Test all functionality**
3. **Deploy frontend** to Netlify/Vercel
4. **Share your app** with users!

## 📞 Support

If you encounter any issues:

1. **Check Render logs** first
2. **Verify environment variables**
3. **Test API endpoints** manually
4. **Check Firebase configuration**

**Render Support**: [help.render.com](https://help.render.com)
**Firebase Support**: [firebase.google.com/support](https://firebase.google.com/support)
