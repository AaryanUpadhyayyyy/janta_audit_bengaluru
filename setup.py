#!/usr/bin/env python3
"""
Setup script for Janata Audit Bengaluru
Initializes the project with sample data and configuration
"""

import os
import sys
import json
from datetime import datetime, timedelta
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from python_scripts.firebase_config import get_firestore_client

def create_sample_data():
    """Create sample data for testing and demonstration"""
    db = get_firestore_client()
    
    print("Creating sample data...")
    
    # Sample projects data
    sample_projects = [
        {
            "projectName": "BBMP Road Widening - MG Road",
            "description": "Widening of MG Road from 4 lanes to 6 lanes to ease traffic congestion",
            "wardNumber": "Ward 1",
            "geoPoint": {"latitude": 12.9716, "longitude": 77.5946},
            "budget": "₹5 Crore",
            "status": "In Progress",
            "department": "BBMP",
            "startDate": datetime.now() - timedelta(days=30),
            "endDate": datetime.now() + timedelta(days=60),
            "contractorName": "ABC Construction Ltd",
            "sourceURL": "https://bbmp.gov.in/projects/mg-road-widening",
            "predictedDelayRisk": "Medium"
        },
        {
            "projectName": "BDA Metro Station Development",
            "description": "Development of new metro station with parking facilities",
            "wardNumber": "Ward 15",
            "geoPoint": {"latitude": 12.9755, "longitude": 77.6000},
            "budget": "₹15 Crore",
            "status": "Completed",
            "department": "BDA",
            "startDate": datetime.now() - timedelta(days=120),
            "endDate": datetime.now() - timedelta(days=30),
            "actualCompletionDate": datetime.now() - timedelta(days=20),
            "contractorName": "XYZ Infrastructure",
            "sourceURL": "https://bdabangalore.org/metro-station",
            "predictedDelayRisk": "Low"
        },
        {
            "projectName": "BWSSB Water Pipeline Extension",
            "description": "Extension of water pipeline to new residential areas",
            "wardNumber": "Ward 25",
            "geoPoint": {"latitude": 12.9600, "longitude": 77.5800},
            "budget": "₹8 Lakh",
            "status": "Pending",
            "department": "BWSSB",
            "startDate": datetime.now() + timedelta(days=15),
            "endDate": datetime.now() + timedelta(days=90),
            "contractorName": "Water Works Ltd",
            "sourceURL": "https://bwssb.karnataka.gov.in/pipeline-extension",
            "predictedDelayRisk": "High"
        },
        {
            "projectName": "BMRCL Metro Line Extension",
            "description": "Extension of metro line from current terminal to airport",
            "wardNumber": "Ward 50",
            "geoPoint": {"latitude": 12.9500, "longitude": 77.6500},
            "budget": "₹200 Crore",
            "status": "In Progress",
            "department": "BMRCL",
            "startDate": datetime.now() - timedelta(days=180),
            "endDate": datetime.now() + timedelta(days=365),
            "contractorName": "Metro Construction Co",
            "sourceURL": "https://english.bmrc.co.in/airport-extension",
            "predictedDelayRisk": "Medium"
        },
        {
            "projectName": "BESCOM Street Light Installation",
            "description": "Installation of LED street lights in residential areas",
            "wardNumber": "Ward 30",
            "geoPoint": {"latitude": 12.9800, "longitude": 77.6200},
            "budget": "₹2 Crore",
            "status": "Completed",
            "department": "BESCOM",
            "startDate": datetime.now() - timedelta(days=60),
            "endDate": datetime.now() - timedelta(days=10),
            "actualCompletionDate": datetime.now() - timedelta(days=5),
            "contractorName": "Electric Solutions Pvt Ltd",
            "sourceURL": "https://bescom.karnataka.gov.in/street-lights",
            "predictedDelayRisk": "Low"
        }
    ]
    
    # Add projects to Firestore
    projects_ref = db.collection('projects')
    for project in sample_projects:
        projects_ref.add(project)
    
    print(f"Added {len(sample_projects)} sample projects")
    
    # Sample political donations data
    sample_donations = [
        {
            "donorName": "ABC Industries",
            "politicalPartyName": "BJP",
            "amount": 5000000,
            "donationDate": datetime.now() - timedelta(days=30),
            "sourceURL": "https://www.eci.gov.in/donations/abc-industries"
        },
        {
            "donorName": "XYZ Corporation",
            "politicalPartyName": "Congress",
            "amount": 3000000,
            "donationDate": datetime.now() - timedelta(days=45),
            "sourceURL": "https://www.eci.gov.in/donations/xyz-corp"
        },
        {
            "donorName": "DEF Construction",
            "politicalPartyName": "JDS",
            "amount": 2000000,
            "donationDate": datetime.now() - timedelta(days=60),
            "sourceURL": "https://www.eci.gov.in/donations/def-construction"
        }
    ]
    
    # Add donations to Firestore
    donations_ref = db.collection('politicalDonations')
    for donation in sample_donations:
        donations_ref.add(donation)
    
    print(f"Added {len(sample_donations)} sample donations")
    
    # Sample AI red flags
    sample_flags = [
        {
            "description": "Unusually high budget for BBMP project: ₹5 Crore (avg: ₹2 Crore)",
            "flagType": "budget_anomaly",
            "linkedProjectIds": [],
            "linkedDonationIds": [],
            "severity": "high",
            "detectedAt": datetime.now()
        },
        {
            "description": "Contractor ABC Construction Ltd has unusually many projects: 5 (avg: 2.1)",
            "flagType": "contractor_anomaly",
            "linkedProjectIds": [],
            "linkedDonationIds": [],
            "severity": "medium",
            "detectedAt": datetime.now()
        }
    ]
    
    # Add AI flags to Firestore
    flags_ref = db.collection('aiRedFlags')
    for flag in sample_flags:
        flags_ref.add(flag)
    
    print(f"Added {len(sample_flags)} sample AI red flags")

def create_environment_template():
    """Create environment template file"""
    env_template = """# Firebase Configuration
REACT_APP_FIREBASE_API_KEY=your_api_key_here
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id

# Google Maps API Key
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Bengaluru coordinates
REACT_APP_BENGALURU_LAT=12.9716
REACT_APP_BENGALURU_LNG=77.5946
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    
    print("Created .env.template file")

def main():
    """Main setup function"""
    print("🚀 Setting up Janata Audit Bengaluru...")
    
    try:
        # Create environment template
        create_environment_template()
        
        # Create sample data
        create_sample_data()
        
        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Copy .env.template to .env and fill in your Firebase credentials")
        print("2. Install dependencies: npm install")
        print("3. Start the development server: npm start")
        print("4. Set up Firebase project and deploy: firebase deploy")
        print("5. Run Python scripts for data scraping and AI analysis")
        print("\n📚 Check README.md for detailed instructions")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        print("Please check your Firebase configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
