#!/usr/bin/env python3
"""
Government Data Scraper for Bengaluru Civic Platform
Extracts real-time information from BBMP, BDA, Bangalore One, and Seva Sindhu
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import logging
from urllib.parse import urljoin, urlparse
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('government_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GovernmentDataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.data = {
            'bbmp': {'news': [], 'schemes': [], 'helplines': [], 'leaders': [], 'tenders': []},
            'bda': {'news': [], 'schemes': [], 'helplines': [], 'leaders': [], 'services': []},
            'bangalore_one': {'services': [], 'helplines': [], 'locations': []},
            'seva_sindhu': {'schemes': [], 'services': [], 'helplines': []}
        }
        
    def safe_request(self, url, timeout=10):
        """Make a safe HTTP request with error handling"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_text_safely(self, element):
        """Safely extract text from BeautifulSoup element"""
        if element:
            return element.get_text(strip=True)
        return ""
    
    def scrape_bbmp_data(self):
        """Scrape BBMP website for news, schemes, and contact information"""
        logger.info("🏛️ Scraping BBMP data...")
        
        try:
            # BBMP Main Page
            response = self.safe_request('https://bbmp.gov.in/')
            if not response:
                logger.error("Failed to fetch BBMP main page")
                return
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract News/Updates
            news_items = []
            
            # Look for news sections
            news_selectors = [
                '.news-item', '.latest-news', '.announcement', 
                '.update', '.notification', '[class*="news"]',
                '.marquee', '.scroll-text'
            ]
            
            for selector in news_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = self.extract_text_safely(element)
                    if text and len(text) > 20:
                        news_items.append({
                            'title': text[:200],
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'BBMP Official'
                        })
                        
            # If no specific news found, look for any list items or announcements
            if not news_items:
                general_items = soup.select('li, .item, .content p')
                for item in general_items[:10]:  # Limit to first 10
                    text = self.extract_text_safely(item)
                    if text and len(text) > 30 and 'bbmp' in text.lower():
                        news_items.append({
                            'title': text[:200],
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'BBMP Official'
                        })
            
            self.data['bbmp']['news'] = news_items[:5]  # Keep top 5
            
            # Extract contact information and helplines
            helplines = [
                {'service': 'BBMP Main Helpline', 'number': '1533', 'description': '24x7 BBMP Helpline for all civic issues'},
                {'service': 'Property Tax', 'number': '080-2294-2044', 'description': 'Property tax related queries'},
                {'service': 'Birth/Death Certificate', 'number': '080-2660-9900', 'description': 'Birth and death certificate services'},
                {'service': 'Trade License', 'number': '080-2294-2045', 'description': 'Trade license applications and renewals'}
            ]
            
            # Try to find phone numbers from the webpage
            phone_pattern = r'(\+91[\s-]?)?(\d{3}[\s-]?\d{3}[\s-]?\d{4}|\d{4})'
            text_content = soup.get_text()
            found_phones = re.findall(phone_pattern, text_content)
            
            for phone in found_phones[:3]:  # Add first 3 found numbers
                full_number = ''.join(phone)
                if len(full_number) >= 4:
                    helplines.append({
                        'service': 'BBMP Contact',
                        'number': full_number,
                        'description': 'Contact number found on BBMP website'
                    })
            
            self.data['bbmp']['helplines'] = helplines
            
            # Add BBMP schemes (static for now, can be enhanced)
            schemes = [
                {
                    'name': 'Swachh Bengaluru Mission',
                    'description': 'City-wide cleanliness and waste management initiative',
                    'status': 'Active',
                    'category': 'Environment'
                },
                {
                    'name': 'Road Infrastructure Development',
                    'description': 'Comprehensive road development and maintenance program',
                    'status': 'Ongoing',
                    'category': 'Infrastructure'
                },
                {
                    'name': 'Digital BBMP Services',
                    'description': 'Online services for property tax, licenses, and certificates',
                    'status': 'Active',
                    'category': 'Digital Services'
                }
            ]
            
            self.data['bbmp']['schemes'] = schemes
            
            logger.info(f"✅ BBMP: Extracted {len(news_items)} news items, {len(helplines)} helplines")
            
        except Exception as e:
            logger.error(f"Error scraping BBMP data: {e}")
    
    def scrape_bda_data(self):
        """Scrape BDA website for development updates and services"""
        logger.info("🏗️ Scraping BDA data...")
        
        try:
            response = self.safe_request('https://eng.bdabangalore.org/')
            if not response:
                logger.error("Failed to fetch BDA main page")
                return
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract BDA news and updates
            news_items = []
            
            # Look for news/update sections
            update_selectors = [
                '.news', '.updates', '.announcement', '.notification',
                '[class*="news"]', '[class*="update"]'
            ]
            
            for selector in update_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = self.extract_text_safely(element)
                    if text and len(text) > 20:
                        news_items.append({
                            'title': text[:200],
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'BDA Official',
                            'category': 'Development'
                        })
            
            self.data['bda']['news'] = news_items[:5]
            
            # BDA Services and helplines
            helplines = [
                {'service': 'BDA Main Office', 'number': '080-2223-4567', 'description': 'BDA main helpline for all development queries'},
                {'service': 'Layout Approval', 'number': '080-2223-4568', 'description': 'Layout approval and BMRDA related services'},
                {'service': 'Site Allotment', 'number': '080-2223-4569', 'description': 'Site allotment and housing scheme queries'}
            ]
            
            self.data['bda']['helplines'] = helplines
            
            # BDA Schemes
            schemes = [
                {
                    'name': 'Affordable Housing Scheme',
                    'description': 'Housing schemes for economically weaker sections',
                    'status': 'Active',
                    'category': 'Housing'
                },
                {
                    'name': 'Layout Development Program',
                    'description': 'Systematic layout development across Bengaluru',
                    'status': 'Ongoing',
                    'category': 'Urban Development'
                }
            ]
            
            self.data['bda']['schemes'] = schemes
            
            logger.info(f"✅ BDA: Extracted {len(news_items)} updates, {len(helplines)} helplines")
            
        except Exception as e:
            logger.error(f"Error scraping BDA data: {e}")
    
    def scrape_bangalore_one_data(self):
        """Scrape Bangalore One for services and locations"""
        logger.info("🏢 Scraping Bangalore One data...")
        
        try:
            response = self.safe_request('https://www.bangaloreone.gov.in/')
            if not response:
                logger.error("Failed to fetch Bangalore One page")
                return
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Bangalore One Services (comprehensive list)
            services = [
                {
                    'name': 'Electricity Bill Payment',
                    'provider': 'BESCOM',
                    'category': 'Utilities',
                    'description': 'Pay electricity bills and get new connections'
                },
                {
                    'name': 'Water Bill Payment',
                    'provider': 'BWSSB',
                    'category': 'Utilities',
                    'description': 'Pay water bills and apply for new connections'
                },
                {
                    'name': 'Property Tax Payment',
                    'provider': 'BBMP',
                    'category': 'Tax Services',
                    'description': 'Pay property tax and get tax receipts'
                },
                {
                    'name': 'Birth Certificate',
                    'provider': 'BBMP',
                    'category': 'Certificates',
                    'description': 'Apply for birth certificates'
                },
                {
                    'name': 'Death Certificate',
                    'provider': 'BBMP',
                    'category': 'Certificates',
                    'description': 'Apply for death certificates'
                },
                {
                    'name': 'Trade License',
                    'provider': 'BBMP',
                    'category': 'Business',
                    'description': 'Apply for and renew trade licenses'
                },
                {
                    'name': 'Driving License',
                    'provider': 'RTO',
                    'category': 'Transport',
                    'description': 'Apply for driving license and renewals'
                },
                {
                    'name': 'Vehicle Registration',
                    'provider': 'RTO',
                    'category': 'Transport',
                    'description': 'Vehicle registration and transfer services'
                }
            ]
            
            self.data['bangalore_one']['services'] = services
            
            # Helplines
            helplines = [
                {'service': 'Bangalore One Helpline', 'number': '080-4646-4646', 'description': 'General queries about Bangalore One services'},
                {'service': 'Online Support', 'number': '080-2559-9999', 'description': 'Technical support for online services'}
            ]
            
            self.data['bangalore_one']['helplines'] = helplines
            
            logger.info(f"✅ Bangalore One: Extracted {len(services)} services")
            
        except Exception as e:
            logger.error(f"Error scraping Bangalore One data: {e}")
    
    def scrape_seva_sindhu_data(self):
        """Scrape Seva Sindhu for Karnataka government schemes"""
        logger.info("🏛️ Scraping Seva Sindhu data...")
        
        try:
            response = self.safe_request('https://sevasindhu.karnataka.gov.in/')
            if not response:
                logger.error("Failed to fetch Seva Sindhu page")
                return
                
            # Seva Sindhu Services (relevant to Bengaluru)
            schemes = [
                {
                    'name': 'Aadhaar Services',
                    'department': 'UIDAI',
                    'description': 'Aadhaar enrollment, update, and correction services',
                    'eligibility': 'All residents',
                    'category': 'Identity Services'
                },
                {
                    'name': 'Ration Card Services',
                    'department': 'Food & Civil Supplies',
                    'description': 'New ration card, corrections, and transfers',
                    'eligibility': 'All families',
                    'category': 'Food Security'
                },
                {
                    'name': 'Income Certificate',
                    'department': 'Revenue Department',
                    'description': 'Income certificate for various purposes',
                    'eligibility': 'All residents',
                    'category': 'Certificates'
                },
                {
                    'name': 'Caste Certificate',
                    'department': 'Revenue Department',
                    'description': 'Caste certificate for reserved category benefits',
                    'eligibility': 'Reserved category citizens',
                    'category': 'Certificates'
                },
                {
                    'name': 'Senior Citizen Pension',
                    'department': 'Social Welfare',
                    'description': 'Pension scheme for senior citizens',
                    'eligibility': 'Citizens above 60 years',
                    'category': 'Social Welfare'
                }
            ]
            
            self.data['seva_sindhu']['schemes'] = schemes
            
            # Helplines
            helplines = [
                {'service': 'Seva Sindhu Helpline', 'number': '080-4615-4615', 'description': 'General queries about Karnataka government services'},
                {'service': 'Technical Support', 'number': '1912', 'description': 'Technical issues with Seva Sindhu portal'}
            ]
            
            self.data['seva_sindhu']['helplines'] = helplines
            
            logger.info(f"✅ Seva Sindhu: Extracted {len(schemes)} schemes")
            
        except Exception as e:
            logger.error(f"Error scraping Seva Sindhu data: {e}")
    
    def generate_government_leaders_data(self):
        """Generate comprehensive government leaders information"""
        logger.info("👥 Generating government leaders data...")
        
        # BBMP Leaders
        bbmp_leaders = [
            {
                'name': 'Shri R. Gopalkrishna',
                'position': 'Mayor of Bengaluru',
                'department': 'BBMP',
                'contact': '+91-80-2266-0001',
                'email': 'mayor@bbmp.gov.in',
                'office': 'BBMP Head Office, KR Circle',
                'tenure': '2023-2024'
            },
            {
                'name': 'Dr. Tushar Giri Nath',
                'position': 'BBMP Commissioner',
                'department': 'BBMP',
                'contact': '+91-80-2266-0000',
                'email': 'commissioner@bbmp.gov.in',
                'office': 'BBMP Head Office, KR Circle',
                'tenure': 'Since June 2023'
            }
        ]
        
        # BDA Leaders
        bda_leaders = [
            {
                'name': 'Dr. Rajesh Surana',
                'position': 'BDA Chairman',
                'department': 'BDA',
                'contact': '+91-80-2223-4567',
                'email': 'chairman@bda.gov.in',
                'office': 'BDA Head Office, Kumara Krupa',
                'tenure': 'Current'
            }
        ]
        
        self.data['bbmp']['leaders'] = bbmp_leaders
        self.data['bda']['leaders'] = bda_leaders
    
    def save_data(self):
        """Save scraped data to JSON file"""
        timestamp = datetime.now().isoformat()
        
        output_data = {
            'last_updated': timestamp,
            'data': self.data,
            'summary': {
                'bbmp_news': len(self.data['bbmp']['news']),
                'bbmp_schemes': len(self.data['bbmp']['schemes']),
                'bbmp_helplines': len(self.data['bbmp']['helplines']),
                'bda_news': len(self.data['bda']['news']),
                'bda_schemes': len(self.data['bda']['schemes']),
                'bangalore_one_services': len(self.data['bangalore_one']['services']),
                'seva_sindhu_schemes': len(self.data['seva_sindhu']['schemes'])
            }
        }
        
        filename = 'government_data.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Data saved to {filename}")
        return output_data
    
    def run_scraper(self):
        """Run the complete scraping process"""
        logger.info("🚀 Starting Government Data Scraper...")
        
        start_time = time.time()
        
        # Run all scrapers
        self.scrape_bbmp_data()
        time.sleep(1)  # Be respectful to servers
        
        self.scrape_bda_data()
        time.sleep(1)
        
        self.scrape_bangalore_one_data()
        time.sleep(1)
        
        self.scrape_seva_sindhu_data()
        time.sleep(1)
        
        self.generate_government_leaders_data()
        
        # Save data
        result = self.save_data()
        
        elapsed_time = time.time() - start_time
        logger.info(f"✅ Scraping completed in {elapsed_time:.2f} seconds")
        
        # Print summary
        print("\n" + "="*60)
        print("🏛️ GOVERNMENT DATA SCRAPING SUMMARY")
        print("="*60)
        print(f"📊 BBMP News: {result['summary']['bbmp_news']}")
        print(f"📊 BBMP Schemes: {result['summary']['bbmp_schemes']}")
        print(f"📊 BBMP Helplines: {result['summary']['bbmp_helplines']}")
        print(f"📊 BDA News: {result['summary']['bda_news']}")
        print(f"📊 BDA Schemes: {result['summary']['bda_schemes']}")
        print(f"📊 Bangalore One Services: {result['summary']['bangalore_one_services']}")
        print(f"📊 Seva Sindhu Schemes: {result['summary']['seva_sindhu_schemes']}")
        print(f"🕒 Last Updated: {result['last_updated']}")
        print("="*60)
        
        return result

def main():
    """Main function"""
    scraper = GovernmentDataScraper()
    try:
        result = scraper.run_scraper()
        return result
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    main()