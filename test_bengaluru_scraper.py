#!/usr/bin/env python3
"""
Quick test script for Bengaluru Project Scraper
"""

import sys
import os
import json
from datetime import datetime

# Add the python_scripts directory to the path
sys.path.append('python_scripts')

try:
    from bengaluru_project_scraper import BengaluruProjectScraper
    
    def test_scraper():
        print("🧪 Testing Bengaluru Project Scraper...")
        print("=" * 50)
        
        # Initialize scraper
        scraper = BengaluruProjectScraper()
        
        try:
            # Test keyword detection
            print("🔍 Testing keyword detection...")
            test_texts = [
                "BBMP road development in Bengaluru",
                "BDA housing scheme in Bangalore",
                "Metro construction in Karnataka",
                "Water supply project in Mumbai",  # Should be filtered out
                "BWSSB infrastructure in Bengaluru"
            ]
            
            for text in test_texts:
                is_related = scraper.is_bengaluru_related(text)
                status = "✅" if is_related else "❌"
                print(f"  {status} '{text}' -> {is_related}")
            
            print("\n🏗️ Testing project extraction...")
            
            # Test a few portals (limited to avoid long execution)
            print("  📊 Testing BBMP portal...")
            scraper.scrape_bbmp_portal()
            
            print("  🏠 Testing BDA portal...")
            scraper.scrape_bda_portal()
            
            print("  💧 Testing BWSSB portal...")
            scraper.scrape_bwssb_portal()
            
            # Show results
            projects = scraper.projects
            print(f"\n📈 Results:")
            print(f"  Total projects found: {len(projects)}")
            
            if projects:
                # Group by source
                sources = {}
                for project in projects:
                    source = project.get('source', 'Unknown')
                    sources[source] = sources.get(source, 0) + 1
                
                print(f"\n📊 Projects by source:")
                for source, count in sources.items():
                    print(f"  {source}: {count}")
                
                # Show sample project
                print(f"\n📋 Sample project:")
                sample = projects[0]
                print(f"  Name: {sample.get('projectName', 'N/A')}")
                print(f"  Source: {sample.get('source', 'N/A')}")
                print(f"  Budget: ₹{sample.get('budget', 0):,}")
                print(f"  Status: {sample.get('status', 'N/A')}")
                print(f"  Location: {sample.get('location', 'N/A')}")
            
            # Save test results
            if projects:
                scraper.save_to_json(projects, 'test_bengaluru_projects.json')
                print(f"\n💾 Test results saved to test_bengaluru_projects.json")
            
            print(f"\n✅ Test completed successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            scraper.close()
    
    if __name__ == "__main__":
        test_scraper()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the project root directory")
    print("💡 Install required packages: pip install requests beautifulsoup4 selenium webdriver-manager lxml pandas")
