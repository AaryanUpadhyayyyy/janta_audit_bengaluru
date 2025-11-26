#!/usr/bin/env python3
"""
Generate comprehensive Bengaluru projects dataset
"""
import json
import random
from datetime import datetime, timedelta

# Bengaluru locations with coordinates
locations = [
    {"name": "Whitefield", "lat": 12.9698, "lng": 77.7499},
    {"name": "Electronic City", "lat": 12.8456, "lng": 77.6601},
    {"name": "Koramangala", "lat": 12.9279, "lng": 77.6271},
    {"name": "Indiranagar", "lat": 12.9719, "lng": 77.6412},
    {"name": "Malleshwaram", "lat": 13.0067, "lng": 77.5751},
    {"name": "Jayanagar", "lat": 12.9250, "lng": 77.5838},
    {"name": "BTM Layout", "lat": 12.9166, "lng": 77.6101},
    {"name": "HSR Layout", "lat": 12.9110, "lng": 77.6462},
    {"name": "Marathahalli", "lat": 12.9592, "lng": 77.6974},
    {"name": "Rajajinagar", "lat": 12.9848, "lng": 77.5567},
    {"name": "Hebbal", "lat": 13.0500, "lng": 77.5900},
    {"name": "Yelahanka", "lat": 13.1007, "lng": 77.5963},
    {"name": "Banashankari", "lat": 12.9250, "lng": 77.5667},
    {"name": "Basavanagudi", "lat": 12.9414, "lng": 77.5670},
    {"name": "Shivajinagar", "lat": 12.9762, "lng": 77.6033},
    {"name": "MG Road", "lat": 12.9716, "lng": 77.5946},
    {"name": "Brigade Road", "lat": 12.9716, "lng": 77.6100},
    {"name": "Commercial Street", "lat": 12.9833, "lng": 77.6167},
    {"name": "KR Puram", "lat": 13.0138, "lng": 77.6928},
    {"name": "Banaswadi", "lat": 13.0192, "lng": 77.6532},
]

# Project types and descriptions
project_types = [
    {
        "type": "Road Infrastructure",
        "projects": [
            "Road Widening Project",
            "Flyover Construction",
            "Bridge Construction", 
            "Junction Improvement",
            "Ring Road Development",
            "Underpass Construction",
            "Traffic Signal Upgrade",
            "Street Lighting Installation",
            "Footpath Development",
            "Median Construction"
        ]
    },
    {
        "type": "Metro & Transport",
        "projects": [
            "Metro Station Construction",
            "Metro Line Extension",
            "Bus Depot Modernization",
            "BMTC Terminal Development",
            "Metro Parking Facility",
            "Bus Rapid Transit System",
            "Transport Hub Development",
            "Metro Commercial Development",
            "Railway Integration Project",
            "Airport Connectivity"
        ]
    },
    {
        "type": "Water & Sanitation",
        "projects": [
            "Water Supply Upgrade",
            "Sewage Treatment Plant",
            "Storm Water Drain",
            "Water Pipeline Installation",
            "Borewell Development",
            "Water Quality Monitoring",
            "Rainwater Harvesting",
            "Flood Management System",
            "Lake Rejuvenation",
            "Wastewater Treatment"
        ]
    },
    {
        "type": "Housing & Development",
        "projects": [
            "Affordable Housing Scheme",
            "Slum Redevelopment Program",
            "IT Park Development",
            "Commercial Complex Construction",
            "Residential Layout Development",
            "Smart City Infrastructure",
            "Urban Forest Development",
            "Park Development",
            "Community Center Construction",
            "Shopping Complex"
        ]
    },
    {
        "type": "Utilities & Services",
        "projects": [
            "Smart Grid Implementation",
            "Solar Installation Program",
            "Digital Governance Platform",
            "Smart Traffic Management",
            "CCTV Surveillance System",
            "Wi-Fi Hotspot Installation",
            "Digital Health Centers",
            "E-Governance Services",
            "Solid Waste Management",
            "Energy Storage System"
        ]
    }
]

departments = ["BBMP", "BDA", "BWSSB", "BMRCL", "BESCOM", "KPWD", "KUIDFC", "BMTC", "PWD", "BBDA"]
statuses = ["Pending", "In Progress", "Completed", "Delayed", "Planning"]
contractors = [
    "L&T Construction", "Nagarjuna Construction", "Simplex Infrastructure", 
    "HCC Limited", "GMR Infrastructure", "DLF Limited", "Sobha Limited",
    "Prestige Group", "Brigade Group", "Embassy Group", "Puravankara Limited",
    "Godrej Properties", "Mahindra Lifespace", "Tata Projects", "Larsen & Toubro"
]

def generate_projects(num_projects=500):
    projects = []
    
    for i in range(num_projects):
        # Select random project type and location
        project_category = random.choice(project_types)
        project_name = random.choice(project_category["projects"])
        location = random.choice(locations)
        
        # Generate random dates
        start_date = datetime.now() - timedelta(days=random.randint(0, 365*2))
        duration = random.randint(180, 1095)  # 6 months to 3 years
        end_date = start_date + timedelta(days=duration)
        
        # Generate budget (in INR)
        base_budget = random.randint(10000000, 500000000)  # 1 crore to 50 crores
        if "Metro" in project_name or "Flyover" in project_name:
            base_budget *= random.randint(2, 10)  # Larger projects
            
        project = {
            "id": f"BBMP_{i+1:04d}",
            "projectName": f"{location['name']} {project_name}",
            "description": f"{project_name} in {location['name']} area to improve infrastructure and connectivity",
            "budget": base_budget,
            "status": random.choice(statuses),
            "location": f"{location['name']}, Bengaluru",
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "department": random.choice(departments),
            "wardNumber": f"Ward {random.randint(1, 198)}",
            "contractor": random.choice(contractors),
            "geoPoint": {
                "latitude": location["lat"] + random.uniform(-0.01, 0.01),
                "longitude": location["lng"] + random.uniform(-0.01, 0.01)
            },
            "progress": random.randint(0, 100) if random.choice(statuses) in ["In Progress", "Completed"] else 0,
            "source": "Karnataka e-Procurement",
            "sourceUrl": "https://eproc.karnataka.gov.in/",
            "scrapedAt": datetime.now().isoformat(),
            "categories": [project_category["type"].lower().replace(" & ", "_").replace(" ", "_")],
            "priority": random.choice(["Low", "Medium", "High"]),
            "dataQuality": {
                "isValid": True,
                "missingFields": [],
                "qualityScore": random.randint(85, 100)
            },
            "estimatedCompletion": random.randint(0, 100),
            "riskAssessment": {
                "level": random.choice(["Low", "Medium", "High"]),
                "score": random.randint(0, 10),
                "factors": []
            }
        }
        
        projects.append(project)
    
    return projects

if __name__ == "__main__":
    print("Generating comprehensive Bengaluru projects dataset...")
    projects = generate_projects(500)  # Generate 500 projects
    
    print(f"Generated {len(projects)} projects")
    
    # Save to file
    with open('bengaluru_projects_new.json', 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
        
    print("Saved to bengaluru_projects_new.json")
    print(f"Sample project: {projects[0]['projectName']}")