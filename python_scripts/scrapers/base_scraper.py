from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime
from typing import List, Dict, Any

class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, base_url: str, collection_name: str):
        self.base_url = base_url
        self.collection_name = collection_name
        self.driver = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def get_page_content(self, url: str) -> BeautifulSoup:
        """Get page content using Selenium"""
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)  # Additional wait for dynamic content
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            self.logger.error(f"Error getting page content from {url}: {str(e)}")
            return None
    
    def extract_text_safely(self, element, default=""):
        """Safely extract text from BeautifulSoup element"""
        if element:
            return element.get_text(strip=True)
        return default
    
    def extract_number_from_text(self, text: str) -> float:
        """Extract number from text, handling Indian number format"""
        if not text:
            return 0.0
        
        # Remove common text and symbols
        text = text.replace(',', '').replace('₹', '').replace('Rs.', '').replace('Lakh', '00000').replace('Crore', '0000000')
        
        # Extract numbers
        import re
        numbers = re.findall(r'[\d.]+', text)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0.0
        return 0.0
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        # Common date formats in Indian government websites
        date_formats = [
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d %B %Y',
            '%d %b %Y',
            '%B %d, %Y',
            '%b %d, %Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        self.logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def get_ward_from_location(self, location: str) -> str:
        """Extract ward number from location string"""
        if not location:
            return "Unknown"
        
        import re
        # Look for ward patterns like "Ward 1", "Ward-1", "Ward No. 1"
        ward_match = re.search(r'[Ww]ard\s*(?:No\.?\s*)?(\d+)', location)
        if ward_match:
            return f"Ward {ward_match.group(1)}"
        
        return "Unknown"
    
    @abstractmethod
    def scrape_projects(self) -> List[Dict[str, Any]]:
        """Scrape projects from the website"""
        pass
    
    @abstractmethod
    def scrape_donations(self) -> List[Dict[str, Any]]:
        """Scrape political donations from the website"""
        pass
    
    def run_scraper(self):
        """Run the scraper and return results"""
        try:
            self.setup_driver()
            self.logger.info(f"Starting to scrape {self.base_url}")
            
            projects = self.scrape_projects()
            donations = self.scrape_donations()
            
            self.logger.info(f"Scraped {len(projects)} projects and {len(donations)} donations")
            
            return {
                'projects': projects,
                'donations': donations
            }
        except Exception as e:
            self.logger.error(f"Error running scraper: {str(e)}")
            return {'projects': [], 'donations': []}
        finally:
            self.close_driver()
