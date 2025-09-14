from .base_scraper import BaseScraper
from datetime import datetime
import re

class BBMPScraper(BaseScraper):
    """Scraper for Bruhat Bengaluru Mahanagara Palike (BBMP) website"""
    
    def __init__(self):
        super().__init__(
            base_url="https://bbmp.gov.in/",
            collection_name="projects"
        )
    
    def scrape_projects(self):
        """Scrape BBMP projects"""
        projects = []
        
        try:
            # Navigate to projects/tenders page
            projects_url = f"{self.base_url}en/tenders"
            soup = self.get_page_content(projects_url)
            
            if not soup:
                return projects
            
            # Look for project listings
            project_elements = soup.find_all(['div', 'tr'], class_=re.compile(r'(project|tender|work)', re.I))
            
            for element in project_elements:
                try:
                    project = self.extract_project_data(element)
                    if project:
                        projects.append(project)
                except Exception as e:
                    self.logger.warning(f"Error extracting project data: {str(e)}")
                    continue
            
            # If no projects found in main page, try other sections
            if not projects:
                projects = self.scrape_from_other_sections()
            
        except Exception as e:
            self.logger.error(f"Error scraping BBMP projects: {str(e)}")
        
        return projects
    
    def extract_project_data(self, element):
        """Extract project data from HTML element"""
        project = {}
        
        # Extract project name
        title_elem = element.find(['h3', 'h4', 'a', 'span'], class_=re.compile(r'(title|name|heading)', re.I))
        if not title_elem:
            title_elem = element.find('a')
        
        if title_elem:
            project['projectName'] = self.extract_text_safely(title_elem)
        
        # Extract description
        desc_elem = element.find(['p', 'div'], class_=re.compile(r'(desc|summary|detail)', re.I))
        if desc_elem:
            project['description'] = self.extract_text_safely(desc_elem)
        
        # Extract budget
        budget_elem = element.find(text=re.compile(r'[₹Rs]?\s*[\d,]+', re.I))
        if budget_elem:
            budget_text = budget_elem.parent.get_text() if hasattr(budget_elem, 'parent') else str(budget_elem)
            project['budget'] = budget_text
        
        # Extract ward information
        ward_elem = element.find(text=re.compile(r'[Ww]ard\s*\d+', re.I))
        if ward_elem:
            ward_text = ward_elem.parent.get_text() if hasattr(ward_elem, 'parent') else str(ward_elem)
            project['wardNumber'] = self.get_ward_from_location(ward_text)
        
        # Extract dates
        date_elem = element.find(text=re.compile(r'\d{1,2}[-/]\d{1,2}[-/]\d{4}', re.I))
        if date_elem:
            date_text = date_elem.parent.get_text() if hasattr(date_elem, 'parent') else str(date_elem)
            parsed_date = self.parse_date(date_text)
            if parsed_date:
                project['startDate'] = parsed_date
        
        # Set default values
        project.setdefault('department', 'BBMP')
        project.setdefault('status', 'In Progress')
        project.setdefault('sourceURL', self.base_url)
        
        # Only return if we have essential data
        if project.get('projectName'):
            return project
        
        return None
    
    def scrape_from_other_sections(self):
        """Scrape projects from other sections of BBMP website"""
        projects = []
        
        try:
            # Try different sections
            sections = [
                'en/works',
                'en/development',
                'en/infrastructure'
            ]
            
            for section in sections:
                section_url = f"{self.base_url}{section}"
                soup = self.get_page_content(section_url)
                
                if soup:
                    # Look for project links or content
                    links = soup.find_all('a', href=re.compile(r'(project|work|tender)', re.I))
                    
                    for link in links:
                        try:
                            project = {
                                'projectName': self.extract_text_safely(link),
                                'description': f"BBMP {section.replace('en/', '').title()} Project",
                                'department': 'BBMP',
                                'status': 'In Progress',
                                'sourceURL': link.get('href', self.base_url),
                                'wardNumber': 'Unknown'
                            }
                            projects.append(project)
                        except Exception as e:
                            self.logger.warning(f"Error processing link: {str(e)}")
                            continue
                
                if projects:
                    break
        
        except Exception as e:
            self.logger.error(f"Error scraping from other sections: {str(e)}")
        
        return projects
    
    def scrape_donations(self):
        """BBMP doesn't typically have political donations, return empty list"""
        return []
