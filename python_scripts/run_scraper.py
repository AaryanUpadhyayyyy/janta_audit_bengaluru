#!/usr/bin/env python3
"""
Script to run the government portal scraper and integrate data
"""

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from government_portal_scraper import GovernmentPortalScraper

def main():
    """Main function to run the scraper and integrate data"""
    print("🚀 Starting Government Portal Scraper...")
    print("=" * 50)
    
    scraper = GovernmentPortalScraper()
    
    try:
        # Scrape all government portals
        print("📊 Scraping government portals...")
        projects = scraper.scrape_all_portals()
        
        print(f"\n✅ Scraping completed!")
        print(f"📈 Total projects found: {len(projects)}")
        
        # Group by source
        sources = {}
        for project in projects:
            source = project.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\n📋 Projects by source:")
        for source, count in sources.items():
            print(f"   {source}: {count}")
        
        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraped_projects_{timestamp}.json"
        scraper.save_to_json(projects, filename)
        
        # Save to Firestore (if configured)
        try:
            scraper.save_to_firestore(projects)
            print("✅ Data saved to Firestore")
        except Exception as e:
            print(f"⚠️  Warning: Could not save to Firestore: {e}")
        
        # Generate summary report
        generate_summary_report(projects, filename)
        
        print(f"\n🎉 Scraping process completed successfully!")
        print(f"📁 Data saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return 1
    finally:
        scraper.close()
    
    return 0

def generate_summary_report(projects, filename):
    """Generate a summary report of scraped projects"""
    report = {
        "scraping_timestamp": datetime.now().isoformat(),
        "total_projects": len(projects),
        "sources": {},
        "status_distribution": {},
        "budget_summary": {
            "total_budget": 0,
            "projects_with_budget": 0,
            "average_budget": 0
        },
        "location_distribution": {},
        "top_departments": {}
    }
    
    # Analyze projects
    total_budget = 0
    budget_count = 0
    
    for project in projects:
        # Source distribution
        source = project.get('source', 'Unknown')
        report["sources"][source] = report["sources"].get(source, 0) + 1
        
        # Status distribution
        status = project.get('status', 'Unknown')
        report["status_distribution"][status] = report["status_distribution"].get(status, 0) + 1
        
        # Budget analysis
        budget = project.get('budget')
        if budget and isinstance(budget, (int, float)):
            total_budget += budget
            budget_count += 1
        
        # Location distribution
        location = project.get('location', 'Unknown')
        report["location_distribution"][location] = report["location_distribution"].get(location, 0) + 1
        
        # Department distribution
        department = project.get('department', 'Unknown')
        report["top_departments"][department] = report["top_departments"].get(department, 0) + 1
    
    # Calculate budget summary
    if budget_count > 0:
        report["budget_summary"]["total_budget"] = total_budget
        report["budget_summary"]["projects_with_budget"] = budget_count
        report["budget_summary"]["average_budget"] = total_budget / budget_count
    
    # Save report
    report_filename = filename.replace('.json', '_report.json')
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Summary report saved to: {report_filename}")
    
    # Print key statistics
    print("\n📈 Key Statistics:")
    print(f"   Total Budget: ₹{total_budget:,.0f}")
    print(f"   Average Budget: ₹{total_budget/budget_count if budget_count > 0 else 0:,.0f}")
    print(f"   Projects with Budget Info: {budget_count}/{len(projects)}")
    
    # Top departments
    sorted_departments = sorted(report["top_departments"].items(), key=lambda x: x[1], reverse=True)
    print(f"\n🏛️  Top Departments:")
    for dept, count in sorted_departments[:5]:
        print(f"   {dept}: {count} projects")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
