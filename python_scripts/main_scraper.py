#!/usr/bin/env python3
"""
Main scraper orchestrator for Janata Audit Bengaluru
Scrapes data from various Bengaluru government websites
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_config import get_firestore_client
from scrapers.bbmp_scraper import BBMPScraper
from scrapers.bda_scraper import BDAScraper
from scrapers.election_commission_scraper import ElectionCommissionScraper

class ScraperOrchestrator:
    """Orchestrates all scrapers and manages data storage"""
    
    def __init__(self):
        self.db = get_firestore_client()
        self.scrapers = [
            BBMPScraper(),
            BDAScraper(),
            ElectionCommissionScraper()
        ]
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def save_projects_to_firestore(self, projects: List[Dict[str, Any]]):
        """Save projects to Firestore"""
        if not projects:
            return
        
        try:
            batch = self.db.batch()
            projects_ref = self.db.collection('projects')
            
            for project in projects:
                # Add metadata
                project['scrapedAt'] = datetime.now()
                project['source'] = 'web_scraper'
                
                # Create document reference
                doc_ref = projects_ref.document()
                batch.set(doc_ref, project)
            
            # Commit batch
            batch.commit()
            self.logger.info(f"Saved {len(projects)} projects to Firestore")
            
        except Exception as e:
            self.logger.error(f"Error saving projects to Firestore: {str(e)}")
    
    def save_donations_to_firestore(self, donations: List[Dict[str, Any]]):
        """Save donations to Firestore"""
        if not donations:
            return
        
        try:
            batch = self.db.batch()
            donations_ref = self.db.collection('politicalDonations')
            
            for donation in donations:
                # Add metadata
                donation['scrapedAt'] = datetime.now()
                donation['source'] = 'web_scraper'
                
                # Create document reference
                doc_ref = donations_ref.document()
                batch.set(doc_ref, donation)
            
            # Commit batch
            batch.commit()
            self.logger.info(f"Saved {len(donations)} donations to Firestore")
            
        except Exception as e:
            self.logger.error(f"Error saving donations to Firestore: {str(e)}")
    
    def run_all_scrapers(self):
        """Run all scrapers and save data to Firestore"""
        total_projects = 0
        total_donations = 0
        
        self.logger.info("Starting data scraping process...")
        
        for scraper in self.scrapers:
            try:
                self.logger.info(f"Running {scraper.__class__.__name__}...")
                
                # Run scraper
                results = scraper.run_scraper()
                
                projects = results.get('projects', [])
                donations = results.get('donations', [])
                
                # Save to Firestore
                if projects:
                    self.save_projects_to_firestore(projects)
                    total_projects += len(projects)
                
                if donations:
                    self.save_donations_to_firestore(donations)
                    total_donations += len(donations)
                
                self.logger.info(f"Completed {scraper.__class__.__name__}: {len(projects)} projects, {len(donations)} donations")
                
            except Exception as e:
                self.logger.error(f"Error running {scraper.__class__.__name__}: {str(e)}")
                continue
        
        self.logger.info(f"Scraping completed. Total: {total_projects} projects, {total_donations} donations")
        
        return {
            'total_projects': total_projects,
            'total_donations': total_donations
        }
    
    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old scraped data"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            # Clean up old projects
            projects_query = self.db.collection('projects').where('scrapedAt', '<', cutoff_date)
            projects_docs = projects_query.get()
            
            for doc in projects_docs:
                doc.reference.delete()
            
            self.logger.info(f"Cleaned up {len(projects_docs)} old project records")
            
            # Clean up old donations
            donations_query = self.db.collection('politicalDonations').where('scrapedAt', '<', cutoff_date)
            donations_docs = donations_query.get()
            
            for doc in donations_docs:
                doc.reference.delete()
            
            self.logger.info(f"Cleaned up {len(donations_docs)} old donation records")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {str(e)}")

def main():
    """Main function"""
    orchestrator = ScraperOrchestrator()
    
    try:
        # Run all scrapers
        results = orchestrator.run_all_scrapers()
        
        # Clean up old data
        orchestrator.cleanup_old_data()
        
        print(f"Scraping completed successfully!")
        print(f"Total projects scraped: {results['total_projects']}")
        print(f"Total donations scraped: {results['total_donations']}")
        
    except Exception as e:
        print(f"Error in main scraper: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
