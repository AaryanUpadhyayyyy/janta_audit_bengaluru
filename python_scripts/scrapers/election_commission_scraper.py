from .base_scraper import BaseScraper
from datetime import datetime
import re

class ElectionCommissionScraper(BaseScraper):
    """Scraper for Election Commission of India donations data"""
    
    def __init__(self):
        super().__init__(
            base_url="https://www.eci.gov.in/",
            collection_name="politicalDonations"
        )
    
    def scrape_projects(self):
        """Election Commission doesn't have projects, return empty list"""
        return []
    
    def scrape_donations(self):
        """Scrape political donations from ECI website"""
        donations = []
        
        try:
            # Navigate to donations/financial statements page
            donations_url = f"{self.base_url}financial-statements"
            soup = self.get_page_content(donations_url)
            
            if not soup:
                return donations
            
            # Look for donation data in tables
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # Skip header row
                    try:
                        donation = self.extract_donation_data(row)
                        if donation:
                            donations.append(donation)
                    except Exception as e:
                        self.logger.warning(f"Error extracting donation data: {str(e)}")
                        continue
            
            # If no donations found in main page, try other sections
            if not donations:
                donations = self.scrape_from_other_sections()
            
        except Exception as e:
            self.logger.error(f"Error scraping ECI donations: {str(e)}")
        
        return donations
    
    def extract_donation_data(self, row):
        """Extract donation data from table row"""
        cells = row.find_all(['td', 'th'])
        
        if len(cells) < 3:
            return None
        
        donation = {}
        
        # Extract donor name (usually first column)
        donor_elem = cells[0].find('a') or cells[0]
        donation['donorName'] = self.extract_text_safely(donor_elem)
        
        # Extract political party (usually second column)
        party_elem = cells[1].find('a') or cells[1]
        donation['politicalPartyName'] = self.extract_text_safely(party_elem)
        
        # Extract amount (usually third column)
        amount_elem = cells[2].find('a') or cells[2]
        amount_text = self.extract_text_safely(amount_elem)
        donation['amount'] = self.extract_number_from_text(amount_text)
        
        # Extract date (usually fourth column)
        if len(cells) > 3:
            date_elem = cells[3].find('a') or cells[3]
            date_text = self.extract_text_safely(date_elem)
            parsed_date = self.parse_date(date_text)
            if parsed_date:
                donation['donationDate'] = parsed_date
        
        # Set source URL
        donation['sourceURL'] = self.base_url
        
        # Only return if we have essential data
        if donation.get('donorName') and donation.get('politicalPartyName'):
            return donation
        
        return None
    
    def scrape_from_other_sections(self):
        """Scrape donations from other sections of ECI website"""
        donations = []
        
        try:
            # Try different sections
            sections = [
                'political-parties',
                'donations',
                'financial-disclosure',
                'election-expenses'
            ]
            
            for section in sections:
                section_url = f"{self.base_url}{section}"
                soup = self.get_page_content(section_url)
                
                if soup:
                    # Look for donation-related content
                    links = soup.find_all('a', href=re.compile(r'(donation|financial|party)', re.I))
                    
                    for link in links:
                        try:
                            # Extract basic info from link text
                            link_text = self.extract_text_safely(link)
                            
                            # Try to extract party name and amount from link text
                            party_match = re.search(r'([A-Za-z\s]+(?:Party|Congress|BJP|Janata))', link_text, re.I)
                            amount_match = re.search(r'[₹Rs]?\s*[\d,]+', link_text)
                            
                            if party_match and amount_match:
                                donation = {
                                    'donorName': 'Unknown',
                                    'politicalPartyName': party_match.group(1).strip(),
                                    'amount': self.extract_number_from_text(amount_match.group(0)),
                                    'donationDate': datetime.now(),
                                    'sourceURL': link.get('href', self.base_url)
                                }
                                donations.append(donation)
                        except Exception as e:
                            self.logger.warning(f"Error processing link: {str(e)}")
                            continue
                
                if donations:
                    break
        
        except Exception as e:
            self.logger.error(f"Error scraping from other sections: {str(e)}")
        
        return donations
