#!/usr/bin/env python3
"""
Government Portal Scraper for Karnataka Infrastructure Projects
Scrapes project data from various Karnataka government portals
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
import pandas as pd
from urllib.parse import urljoin, urlparse
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GovernmentPortalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.projects = []
        self.setup_selenium()
    
    def setup_selenium(self):
        """Setup Selenium WebDriver for dynamic content"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            logger.warning(f"Chrome driver setup failed: {e}")
            self.driver = None
    
    def scrape_eproc_portal(self):
        """Scrape Karnataka e-Procurement Portal"""
        logger.info("Scraping Karnataka e-Procurement Portal...")
        
        try:
            # Main procurement page
            url = "https://eproc.karnataka.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for tender/project links
            project_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(keyword in href.lower() for keyword in ['tender', 'project', 'work', 'contract']):
                    full_url = urljoin(url, href)
                    project_links.append(full_url)
            
            # Extract project details from each link
            for link in project_links[:10]:  # Limit to first 10 for demo
                try:
                    project_data = self.extract_project_details(link, 'e-Procurement')
                    if project_data:
                        self.projects.append(project_data)
                except Exception as e:
                    logger.error(f"Error scraping project from {link}: {e}")
                
                time.sleep(1)  # Be respectful to the server
                
        except Exception as e:
            logger.error(f"Error scraping e-Procurement portal: {e}")
    
    def scrape_bbmp_portal(self):
        """Scrape BBMP Portal"""
        logger.info("Scraping BBMP Portal...")
        
        try:
            url = "https://bbmp.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for project-related content
            project_sections = soup.find_all(['div', 'section'], class_=re.compile(r'project|work|development|infrastructure', re.I))
            
            for section in project_sections:
                project_data = self.extract_bbmp_project(section)
                if project_data:
                    self.projects.append(project_data)
                    
        except Exception as e:
            logger.error(f"Error scraping BBMP portal: {e}")
    
    def scrape_bda_portal(self):
        """Scrape BDA Portal"""
        logger.info("Scraping BDA Portal...")
        
        try:
            url = "https://bdabangalore.org/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for project announcements or news
            news_items = soup.find_all(['div', 'article'], class_=re.compile(r'news|announcement|project|development', re.I))
            
            for item in news_items:
                project_data = self.extract_bda_project(item)
                if project_data:
                    self.projects.append(project_data)
                    
        except Exception as e:
            logger.error(f"Error scraping BDA portal: {e}")
    
    def scrape_bwssb_portal(self):
        """Scrape BWSSB Portal"""
        logger.info("Scraping BWSSB Portal...")
        
        try:
            url = "https://bwssb.karnataka.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for water supply projects
            project_links = soup.find_all('a', href=re.compile(r'project|work|scheme|development', re.I))
            
            for link in project_links[:5]:
                try:
                    project_url = urljoin(url, link['href'])
                    project_data = self.extract_project_details(project_url, 'BWSSB')
                    if project_data:
                        self.projects.append(project_data)
                except Exception as e:
                    logger.error(f"Error scraping BWSSB project: {e}")
                
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error scraping BWSSB portal: {e}")
    
    def scrape_bmrc_portal(self):
        """Scrape BMRCL Portal"""
        logger.info("Scraping BMRCL Portal...")
        
        try:
            url = "https://english.bmrc.co.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for metro project information
            project_sections = soup.find_all(['div', 'section'], class_=re.compile(r'project|phase|line|station', re.I))
            
            for section in project_sections:
                project_data = self.extract_bmrc_project(section)
                if project_data:
                    self.projects.append(project_data)
                    
        except Exception as e:
            logger.error(f"Error scraping BMRCL portal: {e}")
    
    def scrape_bescom_portal(self):
        """Scrape BESCOM Portal"""
        logger.info("Scraping BESCOM Portal...")
        
        try:
            url = "https://bescom.karnataka.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for electrical infrastructure projects
            project_links = soup.find_all('a', href=re.compile(r'project|work|scheme|electrification', re.I))
            
            for link in project_links[:5]:
                try:
                    project_url = urljoin(url, link['href'])
                    project_data = self.extract_project_details(project_url, 'BESCOM')
                    if project_data:
                        self.projects.append(project_data)
                except Exception as e:
                    logger.error(f"Error scraping BESCOM project: {e}")
                
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error scraping BESCOM portal: {e}")
    
    def scrape_kpwd_portal(self):
        """Scrape KPWD Portal"""
        logger.info("Scraping KPWD Portal...")
        
        try:
            url = "https://kpwd.karnataka.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for public works projects
            project_sections = soup.find_all(['div', 'section'], class_=re.compile(r'project|work|road|bridge|building', re.I))
            
            for section in project_sections:
                project_data = self.extract_kpwd_project(section)
                if project_data:
                    self.projects.append(project_data)
                    
        except Exception as e:
            logger.error(f"Error scraping KPWD portal: {e}")
    
    def scrape_kuidfc_portal(self):
        """Scrape KUIDFC Portal"""
        logger.info("Scraping KUIDFC Portal...")
        
        try:
            url = "https://kuidfc.karnataka.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for urban infrastructure projects
            project_links = soup.find_all('a', href=re.compile(r'project|work|scheme|infrastructure', re.I))
            
            for link in project_links[:5]:
                try:
                    project_url = urljoin(url, link['href'])
                    project_data = self.extract_project_details(project_url, 'KUIDFC')
                    if project_data:
                        self.projects.append(project_data)
                except Exception as e:
                    logger.error(f"Error scraping KUIDFC project: {e}")
                
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error scraping KUIDFC portal: {e}")
    
    def scrape_bmtc_portal(self):
        """Scrape BMTC Portal"""
        logger.info("Scraping BMTC Portal...")
        
        try:
            url = "https://mybmtc.karnataka.gov.in/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for transport infrastructure projects
            project_sections = soup.find_all(['div', 'section'], class_=re.compile(r'project|work|route|bus|terminal', re.I))
            
            for section in project_sections:
                project_data = self.extract_bmtc_project(section)
                if project_data:
                    self.projects.append(project_data)
                    
        except Exception as e:
            logger.error(f"Error scraping BMTC portal: {e}")
    
    def extract_project_details(self, url, source):
        """Extract project details from a given URL"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic project information
            title = self.extract_title(soup)
            description = self.extract_description(soup)
            budget = self.extract_budget(soup)
            status = self.extract_status(soup)
            location = self.extract_location(soup)
            start_date = self.extract_date(soup, 'start')
            end_date = self.extract_date(soup, 'end')
            
            if not title:
                return None
            
            project_data = {
                'id': f"{source}_{hash(url)}",
                'projectName': title,
                'description': description or 'No description available',
                'budget': budget,
                'status': status or 'Unknown',
                'location': location,
                'startDate': start_date,
                'endDate': end_date,
                'source': source,
                'sourceUrl': url,
                'scrapedAt': datetime.now().isoformat(),
                'department': source,
                'wardNumber': self.extract_ward_number(soup),
                'contractor': self.extract_contractor(soup),
                'geoPoint': self.extract_coordinates(soup, location)
            }
            
            return project_data
            
        except Exception as e:
            logger.error(f"Error extracting project details from {url}: {e}")
            return None
    
    def extract_title(self, soup):
        """Extract project title"""
        # Try multiple selectors for title
        title_selectors = [
            'h1', 'h2', 'h3',
            '.title', '.project-title', '.tender-title',
            '[class*="title"]', '[class*="heading"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        
        return None
    
    def extract_description(self, soup):
        """Extract project description"""
        # Look for description in various elements
        desc_selectors = [
            '.description', '.project-description', '.content',
            'p', '.summary', '[class*="desc"]'
        ]
        
        for selector in desc_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if len(text) > 50:  # Meaningful description
                    return text[:500]  # Limit length
        
        return None
    
    def extract_budget(self, soup):
        """Extract project budget"""
        text = soup.get_text()
        
        # Look for budget patterns
        budget_patterns = [
            r'₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:crore|crs|lakh|cr)',
            r'Rs\.?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:crore|crs|lakh|cr)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:crore|crs|lakh|cr)',
            r'Budget[:\s]*₹?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = match.group(1).replace(',', '')
                return int(float(amount))
        
        return None
    
    def extract_status(self, soup):
        """Extract project status"""
        text = soup.get_text().lower()
        
        status_keywords = {
            'Completed': ['completed', 'finished', 'done', 'closed'],
            'In Progress': ['progress', 'ongoing', 'running', 'active', 'under construction'],
            'Pending': ['pending', 'waiting', 'not started', 'planned'],
            'Cancelled': ['cancelled', 'cancelled', 'terminated', 'stopped']
        }
        
        for status, keywords in status_keywords.items():
            if any(keyword in text for keyword in keywords):
                return status
        
        return 'Unknown'
    
    def extract_location(self, soup):
        """Extract project location"""
        text = soup.get_text()
        
        # Look for location patterns
        location_patterns = [
            r'Location[:\s]*([^,\n]+)',
            r'Area[:\s]*([^,\n]+)',
            r'Address[:\s]*([^,\n]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Ward|Area|Zone)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return 'Bengaluru'
    
    def extract_date(self, soup, date_type):
        """Extract start or end date"""
        text = soup.get_text()
        
        date_patterns = [
            rf'{date_type.title()}[:\s]*(\d{{1,2}}[/-]\d{{1,2}}[/-]\d{{4}})',
            rf'{date_type.title()}[:\s]*(\d{{4}}[/-]\d{{1,2}}[/-]\d{{1,2}})',
            rf'{date_type.title()}[:\s]*(\w+\s+\d{{1,2}},?\s+\d{{4}})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    date_str = match.group(1)
                    # Try to parse the date
                    for fmt in ['%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y', '%Y-%m-%d', '%B %d, %Y']:
                        try:
                            return datetime.strptime(date_str, fmt).isoformat()
                        except ValueError:
                            continue
                except:
                    continue
        
        return None
    
    def extract_ward_number(self, soup):
        """Extract ward number"""
        text = soup.get_text()
        ward_match = re.search(r'ward\s*(\d+)', text, re.IGNORECASE)
        return int(ward_match.group(1)) if ward_match else None
    
    def extract_contractor(self, soup):
        """Extract contractor information"""
        text = soup.get_text()
        
        contractor_patterns = [
            r'Contractor[:\s]*([^,\n]+)',
            r'Awarded to[:\s]*([^,\n]+)',
            r'Contractor Name[:\s]*([^,\n]+)'
        ]
        
        for pattern in contractor_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_coordinates(self, soup, location):
        """Extract coordinates from location or map elements"""
        # Look for coordinates in the text
        coord_patterns = [
            r'(\d+\.\d+),\s*(\d+\.\d+)',
            r'lat[:\s]*(\d+\.\d+).*lng[:\s]*(\d+\.\d+)',
            r'latitude[:\s]*(\d+\.\d+).*longitude[:\s]*(\d+\.\d+)'
        ]
        
        text = soup.get_text()
        for pattern in coord_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    lat = float(match.group(1))
                    lng = float(match.group(2))
                    return {'latitude': lat, 'longitude': lng}
                except ValueError:
                    continue
        
        # If no coordinates found, use default Bengaluru coordinates
        return {'latitude': 12.9716, 'longitude': 77.5946}
    
    def extract_bbmp_project(self, section):
        """Extract BBMP-specific project data"""
        title = section.find(['h1', 'h2', 'h3', 'h4'])
        if not title:
            return None
        
        return {
            'id': f"BBMP_{hash(str(section))}",
            'projectName': title.get_text(strip=True),
            'description': section.get_text(strip=True)[:500],
            'source': 'BBMP',
            'department': 'BBMP',
            'status': 'In Progress',
            'location': 'Bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946}
        }
    
    def extract_bda_project(self, item):
        """Extract BDA-specific project data"""
        title = item.find(['h1', 'h2', 'h3', 'h4'])
        if not title:
            return None
        
        return {
            'id': f"BDA_{hash(str(item))}",
            'projectName': title.get_text(strip=True),
            'description': item.get_text(strip=True)[:500],
            'source': 'BDA',
            'department': 'BDA',
            'status': 'In Progress',
            'location': 'Bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946}
        }
    
    def extract_bmrc_project(self, section):
        """Extract BMRCL-specific project data"""
        title = section.find(['h1', 'h2', 'h3', 'h4'])
        if not title:
            return None
        
        return {
            'id': f"BMRCL_{hash(str(section))}",
            'projectName': title.get_text(strip=True),
            'description': section.get_text(strip=True)[:500],
            'source': 'BMRCL',
            'department': 'BMRCL',
            'status': 'In Progress',
            'location': 'Bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946}
        }
    
    def extract_kpwd_project(self, section):
        """Extract KPWD-specific project data"""
        title = section.find(['h1', 'h2', 'h3', 'h4'])
        if not title:
            return None
        
        return {
            'id': f"KPWD_{hash(str(section))}",
            'projectName': title.get_text(strip=True),
            'description': section.get_text(strip=True)[:500],
            'source': 'KPWD',
            'department': 'KPWD',
            'status': 'In Progress',
            'location': 'Bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946}
        }
    
    def extract_bmtc_project(self, section):
        """Extract BMTC-specific project data"""
        title = section.find(['h1', 'h2', 'h3', 'h4'])
        if not title:
            return None
        
        return {
            'id': f"BMTC_{hash(str(section))}",
            'projectName': title.get_text(strip=True),
            'description': section.get_text(strip=True)[:500],
            'source': 'BMTC',
            'department': 'BMTC',
            'status': 'In Progress',
            'location': 'Bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946}
        }
    
    def scrape_all_portals(self):
        """Scrape all government portals"""
        logger.info("Starting comprehensive government portal scraping...")
        
        # Scrape all portals
        self.scrape_eproc_portal()
        self.scrape_bbmp_portal()
        self.scrape_bda_portal()
        self.scrape_bwssb_portal()
        self.scrape_bmrc_portal()
        self.scrape_bescom_portal()
        self.scrape_kpwd_portal()
        self.scrape_kuidfc_portal()
        self.scrape_bmtc_portal()
        
        logger.info(f"Scraping completed. Found {len(self.projects)} projects.")
        return self.projects
    
    def save_to_firestore(self, projects):
        """Save projects to Firestore"""
        try:
            from firebase_admin import firestore
            db = firestore.client()
            
            batch = db.batch()
            for project in projects:
                doc_ref = db.collection('projects').document(project['id'])
                batch.set(doc_ref, project)
            
            batch.commit()
            logger.info(f"Saved {len(projects)} projects to Firestore")
            
        except Exception as e:
            logger.error(f"Error saving to Firestore: {e}")
    
    def save_to_json(self, projects, filename='scraped_projects.json'):
        """Save projects to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(projects, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(projects)} projects to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
    
    def close(self):
        """Close selenium driver"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function to run the scraper"""
    scraper = GovernmentPortalScraper()
    
    try:
        # Scrape all portals
        projects = scraper.scrape_all_portals()
        
        # Save results
        scraper.save_to_json(projects)
        scraper.save_to_firestore(projects)
        
        # Print summary
        print(f"\n=== Scraping Summary ===")
        print(f"Total projects found: {len(projects)}")
        
        # Group by source
        sources = {}
        for project in projects:
            source = project.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\nProjects by source:")
        for source, count in sources.items():
            print(f"  {source}: {count}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
