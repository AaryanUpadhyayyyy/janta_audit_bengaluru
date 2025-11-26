# Simple Political Funding Data Scraper (Python)
# This is a simplified version that can run immediately without Firebase
# Run this to populate some initial data for testing

import requests
import pandas as pd
import json
from datetime import datetime
import os

class SimpleFundingScraper:
    def __init__(self):
        self.data_file = 'political_funding_data.json'
        self.scraped_data = []
        
    def scrape_eci_sample_data(self):
        """
        Scrape sample electoral bonds data from ECI or create sample data
        """
        print("🔍 Attempting to scrape ECI Electoral Bonds data...")
        
        # Sample data structure (replace with real scraping when URLs are available)
        sample_eci_data = [
            {
                "source": "ECI_Electoral_Bonds",
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "Future Gaming and Hotel Services Private Limited",
                "recipient_party": "Bharatiya Janata Party",
                "amount": 50000000,  # 5 Crore
                "date_of_purchase": "2023-03-15",
                "date_of_encashment": "2023-03-20",
                "bond_number": "EB001234",
                "is_karnataka_party": True,
                "is_karnataka_donor": False,
                "data_type": "electoral_bond"
            },
            {
                "source": "ECI_Electoral_Bonds", 
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "Bharti Airtel Limited",
                "recipient_party": "Indian National Congress",
                "amount": 25000000,  # 2.5 Crore
                "date_of_purchase": "2023-02-10",
                "date_of_encashment": "2023-02-15", 
                "bond_number": "EB001235",
                "is_karnataka_party": True,
                "is_karnataka_donor": False,
                "data_type": "electoral_bond"
            },
            {
                "source": "ECI_Electoral_Bonds",
                "extraction_date": datetime.now().isoformat(), 
                "donor_name": "Infosys Limited",
                "recipient_party": "Bharatiya Janata Party",
                "amount": 100000000,  # 10 Crore
                "date_of_purchase": "2023-01-20",
                "date_of_encashment": "2023-01-25",
                "bond_number": "EB001236", 
                "is_karnataka_party": True,
                "is_karnataka_donor": True,  # Karnataka company
                "data_type": "electoral_bond"
            },
            {
                "source": "ECI_Electoral_Bonds",
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "Wipro Limited", 
                "recipient_party": "Indian National Congress",
                "amount": 75000000,  # 7.5 Crore
                "date_of_purchase": "2023-04-05",
                "date_of_encashment": "2023-04-10",
                "bond_number": "EB001237",
                "is_karnataka_party": True,
                "is_karnataka_donor": True,  # Karnataka company
                "data_type": "electoral_bond"
            },
            {
                "source": "ECI_Electoral_Bonds",
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "Biocon Limited",
                "recipient_party": "Janata Dal (Secular)",
                "amount": 15000000,  # 1.5 Crore
                "date_of_purchase": "2023-03-01", 
                "date_of_encashment": "2023-03-05",
                "bond_number": "EB001238",
                "is_karnataka_party": True,
                "is_karnataka_donor": True,  # Karnataka company
                "data_type": "electoral_bond"
            }
        ]
        
        self.scraped_data.extend(sample_eci_data)
        print(f"✅ Added {len(sample_eci_data)} ECI sample records")
        
    def scrape_adr_sample_data(self):
        """
        Scrape sample data from ADR India or create sample data
        """
        print("🔍 Attempting to scrape ADR India data...")
        
        # Sample ADR data
        sample_adr_data = [
            {
                "source": "ADR_HTML",
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "DLF Limited",
                "recipient_party": "Bharatiya Janata Party", 
                "amount": 20000000,  # 2 Crore
                "financial_year": "2022-23",
                "is_karnataka_party": True,
                "is_karnataka_donor": False,
                "data_type": "adr_html_table"
            },
            {
                "source": "ADR_HTML",
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "Mindtree Limited",
                "recipient_party": "Indian National Congress",
                "amount": 10000000,  # 1 Crore
                "financial_year": "2022-23", 
                "is_karnataka_party": True,
                "is_karnataka_donor": True,  # Karnataka company
                "data_type": "adr_html_table"
            },
            {
                "source": "ADR_HTML",
                "extraction_date": datetime.now().isoformat(),
                "donor_name": "Tata Consultancy Services",
                "recipient_party": "Bharatiya Janata Party",
                "amount": 55000000,  # 5.5 Crore
                "financial_year": "2022-23",
                "is_karnataka_party": True, 
                "is_karnataka_donor": False,
                "data_type": "adr_html_table"
            }
        ]
        
        self.scraped_data.extend(sample_adr_data)
        print(f"✅ Added {len(sample_adr_data)} ADR sample records")
        
    def generate_anomalies(self):
        """
        Generate sample anomaly/red flag data based on the scraped funding data
        """
        print("🚨 Generating anomaly detection results...")
        
        anomalies = [
            {
                "anomaly_type": "excessive_donation",
                "severity": "HIGH",
                "donor_name": "Future Gaming and Hotel Services Private Limited",
                "recipient_party": "Bharatiya Janata Party", 
                "donation_amount": 50000000,
                "company_capital": 10000000,  # Company capital much lower than donation
                "ratio": 5.0,
                "description": "Donation of ₹5,00,00,000 exceeds 50% of company capital (₹50,00,000)",
                "detection_date": datetime.now().isoformat(),
                "risk_score": 85
            },
            {
                "anomaly_type": "new_company_large_donation", 
                "severity": "HIGH",
                "donor_name": "Future Gaming and Hotel Services Private Limited",
                "recipient_party": "Bharatiya Janata Party",
                "donation_amount": 50000000,
                "registration_date": "2022-12-01",  # Recently incorporated
                "company_age_days": 105,
                "description": "Company incorporated 105 days ago donated ₹5,00,00,000",
                "detection_date": datetime.now().isoformat(),
                "risk_score": 90
            },
            {
                "anomaly_type": "timing_suspicious",
                "severity": "MEDIUM", 
                "donor_name": "Infosys Limited",
                "recipient_party": "Bharatiya Janata Party",
                "donation_amount": 100000000,
                "donation_date": "2023-01-25",
                "election_date": "2023-05-10",  # Karnataka Assembly Elections
                "days_to_election": 105,
                "description": "Large donation of ₹10,00,00,000 made 105 days before election",
                "detection_date": datetime.now().isoformat(),
                "risk_score": 65
            }
        ]
        
        # Save anomalies to separate file
        with open('audit_reports.json', 'w') as f:
            json.dump(anomalies, f, indent=2)
            
        print(f"✅ Generated {len(anomalies)} anomaly reports")
        return anomalies
        
    def save_data(self):
        """
        Save all scraped data to JSON file
        """
        with open(self.data_file, 'w') as f:
            json.dump(self.scraped_data, f, indent=2)
            
        print(f"💾 Saved {len(self.scraped_data)} records to {self.data_file}")
        
    def run_scraping(self):
        """
        Run the complete scraping process
        """
        print("🚀 Starting Political Funding Data Scraping...")
        print("=" * 50)
        
        # Clear existing data
        self.scraped_data = []
        
        # Scrape from different sources
        self.scrape_eci_sample_data()
        self.scrape_adr_sample_data()
        
        # Save the data
        self.save_data()
        
        # Generate anomalies
        anomalies = self.generate_anomalies()
        
        print("=" * 50)
        print("✅ Scraping completed successfully!")
        print(f"📊 Total funding records: {len(self.scraped_data)}")
        print(f"🚨 Total anomalies detected: {len(anomalies)}")
        print(f"💰 Karnataka parties: {len([d for d in self.scraped_data if d.get('is_karnataka_party')])}")
        print(f"🏢 Karnataka donors: {len([d for d in self.scraped_data if d.get('is_karnataka_donor')])}")
        
        return self.scraped_data, anomalies

if __name__ == "__main__":
    scraper = SimpleFundingScraper()
    funding_data, audit_reports = scraper.run_scraping()
    
    print("\n🎯 Next steps:")
    print("1. The data files have been created:")
    print("   - political_funding_data.json")  
    print("   - audit_reports.json")
    print("2. You can now load this data in your web interface")
    print("3. For production, implement real scraping from ECI/ADR websites")