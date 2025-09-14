from .base_scraper import BaseScraper
from datetime import datetime
import re

class BDAScraper(BaseScraper):
    """Scraper for Bangalore Development Authority (BDA) website"""
    
    def __init__(self):
        super().__init__(
            base_url="https://bdabangalore.org/",
            collection_name="projects"
        )
    
    def scrape_projects(self):
        """Scrape BDA projects"""
        projects = []
        
        try:
            # Navigate to projects/tenders page
            projects_url = f"{self.base_url}tenders"
            soup = self.get_page_content(projects_url)
            
            if not soup:
                return projects
            
            # Look for project listings in tables or divs
            project_elements = soup.find_all(['tr', 'div'], class_=re.compile(r'(tender|project|work)', re.I))
            
            for element in project_elements:
                try:
                    project = self.extract_project_data(element)
                    if project:
                        projects.append(project)
                except Exception as e:
                    self.logger.warning(f"Error extracting project data: {str(e)}")
                    continue
            
            # If no projects found, try other sections
            if not projects:
                projects = self.scrape_from_other_sections()
            
        except Exception as e:
            self.logger.error(f"Error scraping BDA projects: {str(e)}")
        
        return projects
    
    def extract_project_data(self, element):
        """Extract project data from HTML element"""
        project = {}
        
        # Extract project name from various possible elements
        title_elem = element.find(['h3', 'h4', 'a', 'td'], class_=re.compile(r'(title|name|heading)', re.I))
        if not title_elem:
            title_elem = element.find('a') or element.find('td')
        
        if title_elem:
            project['projectName'] = self.extract_text_safely(title_elem)
        
        # Extract description
        desc_elem = element.find(['p', 'div', 'td'], class_=re.compile(r'(desc|summary|detail)', re.I))
        if desc_elem:
            project['description'] = self.extract_text_safely(desc_elem)
        
        # Extract budget from text content
        text_content = element.get_text()
        budget_match = re.search(r'[₹Rs]?\s*[\d,]+(?:\s*(?:Lakh|Crore|L|Cr))?', text_content, re.I)
        if budget_match:
            project['budget'] = budget_match.group(0)
        
        # Extract ward information
        ward_match = re.search(r'[Ww]ard\s*\d+', text_content)
        if ward_match:
            project['wardNumber'] = ward_match.group(0)
        
        # Extract dates
        date_match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{4}', text_content)
        if date_match:
            parsed_date = self.parse_date(date_match.group(0))
            if parsed_date:
                project['startDate'] = parsed_date
        
        # Extract contractor name
        contractor_match = re.search(r'[Cc]ontractor[:\s]+([A-Za-z\s&]+)', text_content)
        if contractor_match:
            project['contractorName'] = contractor_match.group(1).strip()
        
        # Set default values
        project.setdefault('department', 'BDA')
        project.setdefault('status', 'In Progress')
        project.setdefault('sourceURL', self.base_url)
        project.setdefault('wardNumber', 'Unknown')
        
        # Only return if we have essential data
        if project.get('projectName'):
            return project
        
        return None
    
    def scrape_from_other_sections(self):
        """Scrape projects from other sections of BDA website"""
        projects = []
        
        try:
            # Try different sections
            sections = [
                'projects',
                'works',
                'development',
                'infrastructure'
            ]
            
            for section in sections:
                section_url = f"{self.base_url}{section}"
                soup = self.get_page_content(section_url)
                
                if soup:
                    # Look for project links or content
                    links = soup.find_all('a', href=re.compile(r'(project|work|tender|development)', re.I))
                    
                    for link in links:
                        try:
                            project = {
                                'projectName': self.extract_text_safely(link),
                                'description': f"BDA {section.title()} Project",
                                'department': 'BDA',
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
        """BDA doesn't typically have political donations, return empty list"""
        return []
