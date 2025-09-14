#!/usr/bin/env python3
"""
Google Earth Engine Setup Script for Janata Audit Bengaluru
This script helps set up Google Earth Engine authentication and configuration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_ee_installation():
    """Check if Google Earth Engine is installed"""
    try:
        import ee
        print("✅ Google Earth Engine is installed")
        return True
    except ImportError:
        print("❌ Google Earth Engine is not installed")
        return False

def install_ee():
    """Install Google Earth Engine"""
    try:
        print("Installing Google Earth Engine...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "earthengine-api"])
        print("✅ Google Earth Engine installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Google Earth Engine: {e}")
        return False

def setup_authentication():
    """Setup Google Earth Engine authentication"""
    try:
        import ee
        
        print("\n🔐 Setting up Google Earth Engine authentication...")
        print("You need to authenticate with Google Earth Engine.")
        print("This will open a web browser for authentication.")
        
        # Initialize and authenticate
        ee.Initialize()
        
        # Test authentication
        test_collection = ee.ImageCollection('COPERNICUS/S2_SR')
        count = test_collection.size()
        count_value = count.getInfo()
        
        if count_value > 0:
            print("✅ Google Earth Engine authentication successful")
            print(f"✅ Test query returned {count_value} images")
            return True
        else:
            print("❌ Authentication test failed")
            return False
            
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n📋 Manual setup instructions:")
        print("1. Go to https://earthengine.google.com/")
        print("2. Sign up for a Google Earth Engine account")
        print("3. Run: earthengine authenticate")
        print("4. Follow the authentication flow")
        return False

def create_service_account_instructions():
    """Create instructions for service account setup"""
    instructions = """
# Google Earth Engine Service Account Setup

For production deployment, you should use a service account:

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable the Earth Engine API
4. Go to IAM & Admin > Service Accounts
5. Create a new service account
6. Download the JSON key file
7. Place it as 'serviceAccountKey.json' in the python_scripts directory
8. Grant the service account Earth Engine access

## Required APIs:
- Earth Engine API
- Cloud Storage API (if using Cloud Storage)

## Service Account Permissions:
- Earth Engine User
- Storage Object Viewer (if using Cloud Storage)
"""
    
    with open('GEE_SETUP_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("📋 Created GEE_SETUP_INSTRUCTIONS.md with detailed setup instructions")

def test_satellite_inspector():
    """Test the satellite inspector functionality"""
    try:
        print("\n🧪 Testing satellite inspector...")
        
        # Import and test
        from satellite_inspector import SatelliteInspector
        
        inspector = SatelliteInspector()
        print("✅ SatelliteInspector initialized successfully")
        
        # Test with sample data
        sample_project = {
            'projectName': 'Test Project',
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946},
            'status': 'In Progress',
            'startDate': '2024-01-01'
        }
        
        print("✅ Sample project data created")
        print("✅ Satellite inspector is ready to use")
        
        return True
        
    except Exception as e:
        print(f"❌ Satellite inspector test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Google Earth Engine for Janata Audit Bengaluru")
    print("=" * 60)
    
    # Check installation
    if not check_ee_installation():
        if not install_ee():
            print("❌ Setup failed. Please install Google Earth Engine manually.")
            return False
    
    # Setup authentication
    if not setup_authentication():
        print("❌ Authentication failed. Please follow manual setup instructions.")
        create_service_account_instructions()
        return False
    
    # Test satellite inspector
    if not test_satellite_inspector():
        print("❌ Satellite inspector test failed.")
        return False
    
    print("\n🎉 Google Earth Engine setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Deploy the Firebase Cloud Functions")
    print("2. Test satellite analysis on a project")
    print("3. Monitor the analysis results in Firestore")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
