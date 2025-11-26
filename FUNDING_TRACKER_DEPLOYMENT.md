# Political Funding Tracker - Firebase Deployment Guide

## Overview
This guide will help you deploy the Political Funding Transparency Tracker to Firebase, including Cloud Functions for comprehensive data extraction and anomaly detection.

## Prerequisites

1. **Firebase Account**: Create a Firebase account at https://firebase.google.com
2. **Node.js**: Install Node.js 18 or later
3. **Firebase CLI**: Install Firebase CLI globally
   ```bash
   npm install -g firebase-tools
   ```
4. **Python 3.9+**: Required for Cloud Functions
5. **System Dependencies** (for PDF processing):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr poppler-utils
   
   # macOS
   brew install tesseract poppler
   
   # Windows
   # Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
   # Install Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
   ```

## Setup Instructions

### 1. Initialize Firebase Project

```bash
# Login to Firebase
firebase login

# Initialize Firebase in your project directory
firebase init

# Select the following services:
# - Functions
# - Firestore
# - Hosting (optional, for web deployment)

# Choose your Firebase project or create a new one
```

### 2. Configure Firestore Database

1. Go to Firebase Console → Firestore Database
2. Create database in production mode
3. Set up the following collections with security rules:

**firestore.rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Political funding data (read-only for authenticated users)
    match /political_funding/{document} {
      allow read: if request.auth != null;
      allow write: if false; // Only Cloud Functions can write
    }
    
    // Audit reports (read-only for authenticated users)  
    match /audit_reports/{document} {
      allow read: if request.auth != null;
      allow write: if false; // Only Cloud Functions can write
    }
    
    // Status collections (read-only)
    match /data_ingestion_status/{document} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    match /anomaly_detection_status/{document} {
      allow read: if request.auth != null;
      allow write: if false;
    }
  }
}
```

### 3. Set up Cloud Functions

```bash
# Navigate to functions directory
cd functions

# Install Python dependencies
pip install -r requirements.txt

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `functions/.env` file:
```bash
# MCA API Configuration (if available)
MCA_API_KEY=your_mca_api_key_here
MCA_BASE_URL=https://www.mca.gov.in

# ECI Configuration
ECI_BASE_URL=https://www.eci.gov.in

# ADR Configuration  
ADR_BASE_URL=https://adrindia.org

# Tesseract configuration (if custom path needed)
TESSERACT_CMD=/usr/bin/tesseract

# PDF processing configuration
PDF_TIMEOUT_SECONDS=120
MAX_PDF_SIZE_MB=50
```

### 5. Deploy Cloud Functions

```bash
# Deploy all functions
firebase deploy --only functions

# Deploy specific function
firebase deploy --only functions:scheduled_data_ingestion
firebase deploy --only functions:scheduled_anomaly_detection
firebase deploy --only functions:manual_data_refresh
firebase deploy --only functions:manual_anomaly_analysis
```

### 6. Set up Firestore Indexes

Create `firestore.indexes.json`:
```json
{
  "indexes": [
    {
      "collectionGroup": "political_funding",
      "queryScope": "COLLECTION",
      "fields": [
        {"fieldPath": "extraction_date", "order": "DESCENDING"},
        {"fieldPath": "is_karnataka_party", "order": "ASCENDING"}
      ]
    },
    {
      "collectionGroup": "political_funding", 
      "queryScope": "COLLECTION",
      "fields": [
        {"fieldPath": "amount", "order": "DESCENDING"},
        {"fieldPath": "is_karnataka_donor", "order": "ASCENDING"}
      ]
    },
    {
      "collectionGroup": "audit_reports",
      "queryScope": "COLLECTION", 
      "fields": [
        {"fieldPath": "detection_date", "order": "DESCENDING"},
        {"fieldPath": "severity", "order": "ASCENDING"}
      ]
    },
    {
      "collectionGroup": "audit_reports",
      "queryScope": "COLLECTION",
      "fields": [
        {"fieldPath": "risk_score", "order": "DESCENDING"},
        {"fieldPath": "anomaly_type", "order": "ASCENDING"}
      ]
    }
  ],
  "fieldOverrides": []
}
```

Deploy indexes:
```bash
firebase deploy --only firestore:indexes
```

## Cloud Functions Details

### 1. Data Ingestion Engine (`main.py`)

**Function: `scheduled_data_ingestion`**
- **Trigger**: Scheduled (daily at 2 AM)
- **Purpose**: Extract data from ECI, ADR sources with comprehensive PDF processing
- **Features**:
  - Dual-method PDF extraction (pdfplumber + OCR)
  - CSV parsing from ECI
  - HTML table extraction from ADR
  - MCA data enrichment
  - Complete data capture (no information left behind)

**Function: `manual_data_refresh`**
- **Trigger**: HTTP
- **URL**: `https://your-project.cloudfunctions.net/manual_data_refresh`
- **Parameters**: `?source=eci|adr|all`

### 2. Anomaly Detection Engine (`anomaly_detection.py`)

**Function: `scheduled_anomaly_detection`**
- **Trigger**: Scheduled (daily at 6 AM)
- **Purpose**: Analyze funding data for suspicious patterns
- **Detection Types**:
  - Excessive donations vs company profits
  - Shell company indicators
  - Suspicious timing near elections
  - New company large donations
  - Round number patterns
  - Address clustering
  - Dormant company activity
  - Disproportionate donations

**Function: `manual_anomaly_analysis`**
- **Trigger**: HTTP
- **URL**: `https://your-project.cloudfunctions.net/manual_anomaly_analysis`

## Frontend Integration

### 1. Update Firebase Configuration

In your `index.html`, update the Firebase configuration:
```javascript
// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
```

### 2. Deploy Frontend

```bash
# Build and deploy to Firebase Hosting
firebase deploy --only hosting
```

## Testing the System

### 1. Test Data Ingestion

```bash
# Trigger manual data refresh
curl -X POST "https://your-project.cloudfunctions.net/manual_data_refresh?source=all"

# Check logs
firebase functions:log
```

### 2. Test Anomaly Detection

```bash
# Trigger manual anomaly analysis
curl -X POST "https://your-project.cloudfunctions.net/manual_anomaly_analysis"

# Monitor Firestore for results
```

### 3. Verify Frontend Integration

1. Open your deployed website
2. Navigate to "Funding Audit" tab
3. Check that data loads properly
4. Test search and filter functionality
5. Verify audit reports display

## Monitoring and Maintenance

### 1. Set up Cloud Monitoring

- Monitor Cloud Function execution
- Set up alerts for failures
- Track Firestore usage

### 2. Regular Updates

- Update PDF source URLs as they change
- Monitor ECI and ADR websites for structure changes
- Update anomaly detection thresholds based on findings

### 3. Data Quality Checks

- Regularly verify data extraction completeness
- Monitor for missing or corrupted records
- Validate anomaly detection accuracy

## Security Considerations

1. **API Keys**: Keep all API keys secure and rotate regularly
2. **Firestore Rules**: Ensure proper read/write permissions
3. **Function Authentication**: Consider adding authentication for manual triggers
4. **Data Privacy**: Ensure compliance with data protection regulations

## Troubleshooting

### Common Issues:

1. **PDF Processing Fails**: Check Tesseract and Poppler installation
2. **Memory Limits**: Increase Cloud Function memory for large PDF processing
3. **Timeout Issues**: Adjust function timeout settings
4. **Firestore Permission Errors**: Check security rules
5. **Missing Data**: Verify source URLs and extraction logic

### Debug Commands:

```bash
# View function logs
firebase functions:log --only scheduled_data_ingestion

# Test functions locally
firebase emulators:start --only functions,firestore

# Check Firestore data
firebase firestore:data-export gs://your-bucket/exports
```

## Performance Optimization

1. **Batch Processing**: Process large datasets in batches
2. **Caching**: Implement result caching for repeated queries
3. **Indexing**: Create appropriate Firestore indexes
4. **Memory Management**: Optimize memory usage in PDF processing
5. **Parallel Processing**: Process multiple PDFs concurrently

## Cost Optimization

1. **Function Execution**: Optimize function runtime
2. **Firestore Usage**: Minimize unnecessary reads/writes
3. **Storage**: Clean up old data periodically
4. **Bandwidth**: Compress data where possible

This deployment guide ensures your Political Funding Transparency Tracker is production-ready with comprehensive data extraction, advanced anomaly detection, and a user-friendly interface.