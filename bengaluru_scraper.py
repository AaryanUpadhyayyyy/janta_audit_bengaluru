import json
import random
import time
from datetime import datetime, timedelta

def generate_mock_projects():
    """Generates a list of new mock project data."""
    
    project_names = [
        "Lake Rejuvenation Project", "Flyover Construction", "Community Hall Renovation",
        "Smart Parking System", "Public Park Development", "Stormwater Drain Upgrade",
        "LED Streetlight Installation", "Waste Management Facility", "Pedestrian Skywalk",
        "Urban Forest Initiative"
    ]
    
    departments = ["BBMP", "BDA", "BWSSB", "BESCOM", "KPWD"]
    statuses = ["In Progress", "Pending", "Completed"]
    locations = [
        "Koramangala", "Indiranagar", "Jayanagar", "Whitefield", "HSR Layout",
        "Electronic City", "Marathahalli", "Yelahanka", "Hebbal", "Malleshwaram"
    ]

    new_projects = []
    for i in range(random.randint(5, 10)): # Generate 5 to 10 new projects
        start_date = datetime.now() - timedelta(days=random.randint(30, 365))
        end_date = start_date + timedelta(days=random.randint(180, 730))
        
        project = {
            'id': f'proj_{int(time.time())}_{i}',
            'projectName': f"{random.choice(project_names)} - {random.choice(locations)}",
            'description': f"A new project to improve infrastructure in {random.choice(locations)}.",
            'status': random.choice(statuses),
            'budget': random.randint(1000000, 500000000), # 10 Lakhs to 50 Crores
            'location': f"{random.choice(locations)}, Bengaluru, Karnataka",
            'department': random.choice(departments),
            'wardNumber': random.randint(1, 198),
            'geoPoint': {
                'latitude': round(random.uniform(12.8, 13.1), 6),
                'longitude': round(random.uniform(77.5, 77.8), 6)
            },
            'contractor': f"Contractor_{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])}",
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'source': 'Scraped from Mock Data Portal',
            'sourceUrl': 'http://mock.example.com/projects',
            'scrapedAt': datetime.now().isoformat()
        }
        new_projects.append(project)
        
    return new_projects

def main():
    """Main function to run the scraper."""
    print("Starting Bengaluru Projects Scraper...")
    
    try:
        # Load existing projects if the file exists
        try:
            with open('bengaluru_projects.json', 'r', encoding='utf-8') as f:
                existing_projects = json.load(f)
            print(f"Found {len(existing_projects)} existing projects.")
        except (FileNotFoundError, json.JSONDecodeError):
            existing_projects = []
            print("No existing project file found. Starting fresh.")

        # Generate new mock projects
        new_projects = generate_mock_projects()
        print(f"Generated {len(new_projects)} new projects.")
        
        # Combine and save
        # A real scraper might merge based on ID, but here we'll just append for simplicity
        all_projects = existing_projects + new_projects
        
        with open('bengaluru_projects.json', 'w', encoding='utf-8') as f:
            json.dump(all_projects, f, indent=4)
            
        print(f"Successfully scraped and saved {len(all_projects)} total projects to bengaluru_projects.json")
        
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == "__main__":
    main()
