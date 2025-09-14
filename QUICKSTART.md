# 🚀 Quick Start Guide - Janata Audit Bengaluru

Get up and running with Janata Audit Bengaluru in 5 minutes!

## Prerequisites Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.8+ installed
- [ ] Google Cloud Platform account
- [ ] Firebase project created
- [ ] Google Maps API key obtained

## Step 1: Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd janata-audit-bengaluru

# Install frontend dependencies
npm install

# Install Python dependencies
cd python_scripts
pip install -r requirements.txt
cd ..
```

## Step 2: Firebase Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Firestore Database
   - Enable Authentication (Phone provider)
   - Enable Cloud Functions

2. **Get Firebase Config**
   - Go to Project Settings > General
   - Copy your Firebase config values

3. **Create Environment File**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your Firebase credentials:
   ```env
   REACT_APP_FIREBASE_API_KEY=your_api_key
   REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   REACT_APP_FIREBASE_PROJECT_ID=your_project_id
   REACT_APP_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   REACT_APP_FIREBASE_APP_ID=your_app_id
   REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```

## Step 3: Deploy Backend

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase (if not already done)
firebase init

# Deploy everything
firebase deploy
```

## Step 4: Run the Application

```bash
# Start the development server
npm start
```

Visit `http://localhost:3000` to see your application!

## Step 5: Add Sample Data (Optional)

```bash
# Run the setup script to add sample data
python setup.py
```

## Step 6: Run Data Scraping (Optional)

```bash
cd python_scripts

# Run data scraping
python main_scraper.py

# Train ML model
python model_trainer.py

# Run AI analysis
python ai_brain.py
```

## 🎉 You're Done!

Your Janata Audit Bengaluru platform is now running locally. 

### What's Next?

1. **Customize the UI**: Modify components in `src/components/`
2. **Add More Data Sources**: Extend scrapers in `python_scripts/scrapers/`
3. **Improve AI Models**: Enhance ML models in `python_scripts/`
4. **Deploy to Production**: Use `deploy.bat` (Windows) or `deploy.sh` (Linux/Mac)

### Troubleshooting

**Firebase Authentication Issues**
- Ensure phone authentication is enabled in Firebase Console
- Check that your API keys are correct

**Google Maps Not Loading**
- Verify your Google Maps API key is valid
- Enable the Maps JavaScript API in Google Cloud Console

**Python Scripts Failing**
- Ensure you have the service account key file
- Check that all dependencies are installed

### Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review the code comments for implementation details
- Create an issue in the GitHub repository

---

**Happy Coding! 🎯**
