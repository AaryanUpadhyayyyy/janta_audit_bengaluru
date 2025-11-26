#!/usr/bin/env python3
"""
Real-time Government Data Update System
Automatically scrapes and updates government data at regular intervals
"""

import schedule
import time
import threading
import json
import os
from datetime import datetime, timedelta
from government_data_scraper import GovernmentDataScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeUpdater:
    def __init__(self, update_interval_hours=6):
        self.update_interval = update_interval_hours
        self.scraper = GovernmentDataScraper()
        self.last_update = None
        self.is_running = False
        
    def update_government_data(self):
        """Update government data and log the process"""
        logger.info("🔄 Starting scheduled government data update...")
        
        try:
            result = self.scraper.run_scraper()
            if result:
                self.last_update = datetime.now()
                logger.info(f"✅ Government data updated successfully at {self.last_update}")
                
                # Create a status file for the web interface
                status = {
                    'last_update': self.last_update.isoformat(),
                    'next_update': (self.last_update + timedelta(hours=self.update_interval)).isoformat(),
                    'status': 'success',
                    'summary': result.get('summary', {})
                }
                
                with open('update_status.json', 'w') as f:
                    json.dump(status, f, indent=2)
                    
            else:
                logger.error("❌ Government data update failed")
                
        except Exception as e:
            logger.error(f"❌ Error during government data update: {e}")
    
    def start_scheduler(self):
        """Start the automatic update scheduler"""
        logger.info(f"🚀 Starting real-time government data updater (every {self.update_interval} hours)")
        
        # Schedule updates
        schedule.every(self.update_interval).hours.do(self.update_government_data)
        
        # Run initial update
        self.update_government_data()
        
        self.is_running = True
        
        # Keep the scheduler running
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def start_background(self):
        """Start the updater in background thread"""
        if not self.is_running:
            thread = threading.Thread(target=self.start_scheduler, daemon=True)
            thread.start()
            logger.info("📡 Background government data updater started")
    
    def stop(self):
        """Stop the updater"""
        self.is_running = False
        logger.info("⏹️ Government data updater stopped")

# Global updater instance
updater = None

def start_real_time_updates():
    """Start real-time updates (can be called from other modules)"""
    global updater
    if not updater or not updater.is_running:
        updater = RealTimeUpdater(update_interval_hours=6)  # Update every 6 hours
        updater.start_background()
    
def get_update_status():
    """Get current update status"""
    try:
        with open('update_status.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'last_update': None,
            'next_update': None,
            'status': 'pending',
            'summary': {}
        }

if __name__ == "__main__":
    # Run as standalone
    updater = RealTimeUpdater(update_interval_hours=1)  # Update every hour for testing
    try:
        updater.start_scheduler()
    except KeyboardInterrupt:
        logger.info("Real-time updater stopped by user")
        updater.stop()