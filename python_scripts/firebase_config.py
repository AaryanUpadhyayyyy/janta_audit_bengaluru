import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        # Use service account key file or environment variables
        if os.path.exists('serviceAccountKey.json'):
            cred = credentials.Certificate('serviceAccountKey.json')
        else:
            # Use default credentials (for production)
            cred = credentials.ApplicationDefault()
        
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

def get_firestore_client():
    """Get Firestore client instance"""
    return initialize_firebase()
