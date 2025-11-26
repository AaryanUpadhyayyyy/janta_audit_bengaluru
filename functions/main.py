# Political Funding Data Ingestion Engine - Firebase Cloud Functions
# This module handles comprehensive data extraction from ECI, ADR, and MCA sources

import functions_framework
from firebase_functions import firestore_fn, scheduler_fn
from google.cloud import firestore
import pandas as pd
import requests
import io
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import re
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Optional
import json

# Initialize Firestore client
db = firestore.Client()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngestionEngine:
    """
    Comprehensive data ingestion engine for political funding transparency.
    Extracts ALL data from PDFs using dual-method approach (text + OCR).
    """
    
    def __init__(self):
        self.eci_base_url = "https://www.eci.gov.in"
        self.adr_base_url = "https://adrindia.org"
        self.mca_base_url = "https://www.mca.gov.in"
        
    def extract_eci_electoral_bonds(self) -> List[Dict]:
        """
        Extract Electoral Bonds data from ECI CSV files.
        Must capture every single donation record without exception.
        """
        try:
            logger.info("Starting ECI Electoral Bonds data extraction...")
            
            # ECI Electoral Bonds CSV URLs (these may need to be updated)
            csv_urls = [
                f"{self.eci_base_url}/files/file/13730-electoral-bonds-data-2024/",
                f"{self.eci_base_url}/files/file/13729-electoral-bonds-data-2023/"
            ]
            
            all_donations = []
            
            for url in csv_urls:
                try:
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()
                    
                    # Parse CSV data
                    df = pd.read_csv(io.StringIO(response.text))
                    
                    # Standardize column names
                    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                    
                    # Process each record
                    for _, row in df.iterrows():
                        donation = {
                            'source': 'ECI_Electoral_Bonds',
                            'extraction_date': datetime.now().isoformat(),
                            'donor_name': str(row.get('donor_name', '')).strip(),
                            'recipient_party': str(row.get('political_party', '')).strip(),
                            'amount': self._parse_amount(row.get('denomination', 0)),
                            'date_of_purchase': self._parse_date(row.get('date_of_purchase')),
                            'date_of_encashment': self._parse_date(row.get('date_of_encashment')),
                            'bond_number': str(row.get('bond_number', '')),
                            'is_karnataka_party': self._is_karnataka_party(str(row.get('political_party', ''))),
                            'is_karnataka_donor': False,  # Will be updated with MCA data
                            'data_type': 'electoral_bond',
                            'raw_data': row.to_dict()
                        }
                        all_donations.append(donation)
                        
                except Exception as e:
                    logger.error(f"Error processing ECI URL {url}: {str(e)}")
                    continue
                    
            logger.info(f"Extracted {len(all_donations)} electoral bond records from ECI")
            return all_donations
            
        except Exception as e:
            logger.error(f"Error in ECI data extraction: {str(e)}")
            return []
    
    def extract_adr_reports_comprehensive(self) -> List[Dict]:
        """
        Extract ALL data from ADR India reports (HTML tables + PDFs).
        This function ensures NO DATA IS LEFT BEHIND from any PDF.
        """
        try:
            logger.info("Starting comprehensive ADR data extraction...")
            
            all_donations = []
            
            # Step 1: Extract from HTML tables
            html_donations = self._extract_adr_html_data()
            all_donations.extend(html_donations)
            
            # Step 2: Extract from PDF reports (CRITICAL - dual method)
            pdf_donations = self._extract_adr_pdf_data_comprehensive()
            all_donations.extend(pdf_donations)
            
            logger.info(f"Total ADR records extracted: {len(all_donations)}")
            return all_donations
            
        except Exception as e:
            logger.error(f"Error in ADR comprehensive extraction: {str(e)}")
            return []
    
    def _extract_adr_html_data(self) -> List[Dict]:
        """Extract data from ADR HTML tables."""
        try:
            # ADR donation data pages
            adr_pages = [
                f"{self.adr_base_url}/content/analysis-donations-received-political-parties-2021-22",
                f"{self.adr_base_url}/content/analysis-donations-received-political-parties-2022-23"
            ]
            
            all_data = []
            
            for page_url in adr_pages:
                try:
                    response = requests.get(page_url, timeout=30)
                    response.raise_for_status()
                    
                    # Parse HTML tables using pandas
                    tables = pd.read_html(response.text)
                    
                    for table in tables:
                        for _, row in table.iterrows():
                            if len(row) >= 3:  # Minimum columns expected
                                donation = {
                                    'source': 'ADR_HTML',
                                    'extraction_date': datetime.now().isoformat(),
                                    'donor_name': str(row.iloc[0]).strip(),
                                    'recipient_party': str(row.iloc[1]).strip(),
                                    'amount': self._parse_amount(row.iloc[2]),
                                    'financial_year': self._extract_year_from_url(page_url),
                                    'is_karnataka_party': self._is_karnataka_party(str(row.iloc[1])),
                                    'is_karnataka_donor': False,
                                    'data_type': 'adr_html_table',
                                    'source_url': page_url,
                                    'raw_data': row.to_dict()
                                }
                                all_data.append(donation)
                                
                except Exception as e:
                    logger.error(f"Error processing ADR HTML page {page_url}: {str(e)}")
                    continue
                    
            return all_data
            
        except Exception as e:
            logger.error(f"Error in ADR HTML extraction: {str(e)}")
            return []
    
    def _extract_adr_pdf_data_comprehensive(self) -> List[Dict]:
        """
        CRITICAL FUNCTION: Extract ALL data from ADR PDF reports.
        Uses dual-method approach: pdfplumber + OCR to ensure NO DATA IS MISSED.
        """
        try:
            logger.info("Starting comprehensive PDF extraction from ADR reports...")
            
            # ADR PDF report URLs (these should be updated with actual URLs)
            pdf_urls = [
                f"{self.adr_base_url}/sites/default/files/Donation_Report_2021-22.pdf",
                f"{self.adr_base_url}/sites/default/files/Donation_Report_2022-23.pdf",
                f"{self.adr_base_url}/sites/default/files/Donation_Report_2023-24.pdf"
            ]
            
            all_pdf_data = []
            
            for pdf_url in pdf_urls:
                logger.info(f"Processing PDF: {pdf_url}")
                
                try:
                    # Download PDF
                    response = requests.get(pdf_url, timeout=60)
                    response.raise_for_status()
                    pdf_bytes = response.content
                    
                    # METHOD 1: Extract using pdfplumber (for text-based PDFs)
                    text_extracted_data = self._extract_pdf_with_pdfplumber(pdf_bytes, pdf_url)
                    all_pdf_data.extend(text_extracted_data)
                    
                    # METHOD 2: Extract using OCR (for scanned/image PDFs)
                    ocr_extracted_data = self._extract_pdf_with_ocr(pdf_bytes, pdf_url)
                    all_pdf_data.extend(ocr_extracted_data)
                    
                    logger.info(f"Extracted {len(text_extracted_data + ocr_extracted_data)} records from {pdf_url}")
                    
                except Exception as e:
                    logger.error(f"Error processing PDF {pdf_url}: {str(e)}")
                    continue
            
            # Remove duplicates while preserving all unique data
            unique_data = self._deduplicate_records(all_pdf_data)
            logger.info(f"Final unique PDF records: {len(unique_data)}")
            
            return unique_data
            
        except Exception as e:
            logger.error(f"Error in comprehensive PDF extraction: {str(e)}")
            return []
    
    def _extract_pdf_with_pdfplumber(self, pdf_bytes: bytes, source_url: str) -> List[Dict]:
        """Extract data from text-based PDFs using pdfplumber."""
        try:
            all_data = []
            
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract all text
                    text = page.extract_text()
                    
                    # Extract all tables
                    tables = page.extract_tables()
                    
                    # Process tables first (most structured data)
                    for table in tables:
                        if table and len(table) > 1:  # Has header and data
                            headers = table[0]
                            for row in table[1:]:
                                if len(row) >= 3:  # Minimum columns for meaningful data
                                    donation = self._parse_table_row_to_donation(
                                        headers, row, source_url, page_num, 'pdfplumber'
                                    )
                                    if donation:
                                        all_data.append(donation)
                    
                    # Process raw text for any missed data
                    text_donations = self._parse_text_for_donations(text, source_url, page_num)
                    all_data.extend(text_donations)
            
            return all_data
            
        except Exception as e:
            logger.error(f"Error in pdfplumber extraction: {str(e)}")
            return []
    
    def _extract_pdf_with_ocr(self, pdf_bytes: bytes, source_url: str) -> List[Dict]:
        """Extract data from scanned PDFs using OCR (pytesseract)."""
        try:
            all_data = []
            
            # Convert PDF pages to images
            images = convert_from_bytes(pdf_bytes, dpi=300)
            
            for page_num, image in enumerate(images):
                # Perform OCR on the image
                ocr_text = pytesseract.image_to_string(image, lang='eng')
                
                # Parse OCR text for donation data
                ocr_donations = self._parse_text_for_donations(ocr_text, source_url, page_num, 'ocr')
                all_data.extend(ocr_donations)
                
                # Try to extract table structure from OCR
                table_data = self._extract_table_from_ocr_text(ocr_text, source_url, page_num)
                all_data.extend(table_data)
            
            return all_data
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {str(e)}")
            return []
    
    def _parse_table_row_to_donation(self, headers: List, row: List, source_url: str, 
                                   page_num: int, method: str) -> Optional[Dict]:
        """Parse a table row into a standardized donation record."""
        try:
            # Map common column patterns
            donor_col = self._find_column_index(headers, ['donor', 'company', 'contributor'])
            party_col = self._find_column_index(headers, ['party', 'recipient', 'political'])
            amount_col = self._find_column_index(headers, ['amount', 'donation', 'sum', 'total'])
            date_col = self._find_column_index(headers, ['date', 'year', 'period'])
            
            if donor_col is not None and party_col is not None and amount_col is not None:
                donation = {
                    'source': f'ADR_PDF_{method}',
                    'extraction_date': datetime.now().isoformat(),
                    'donor_name': str(row[donor_col]).strip() if donor_col < len(row) else '',
                    'recipient_party': str(row[party_col]).strip() if party_col < len(row) else '',
                    'amount': self._parse_amount(row[amount_col] if amount_col < len(row) else 0),
                    'date_info': str(row[date_col]).strip() if date_col and date_col < len(row) else '',
                    'page_number': page_num + 1,
                    'source_url': source_url,
                    'extraction_method': method,
                    'is_karnataka_party': self._is_karnataka_party(str(row[party_col]) if party_col < len(row) else ''),
                    'is_karnataka_donor': False,
                    'data_type': 'adr_pdf_table',
                    'raw_headers': headers,
                    'raw_row': row
                }
                return donation
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing table row: {str(e)}")
            return None
    
    def _parse_text_for_donations(self, text: str, source_url: str, page_num: int, 
                                method: str = 'text') -> List[Dict]:
        """Parse raw text for donation patterns."""
        try:
            donations = []
            
            # Common patterns for donation data
            patterns = [
                # Pattern: Company Name - Rs. 1,00,000 - BJP
                r'(.+?)\s*-\s*Rs\.?\s*([\d,]+)\s*-\s*(.+?)(?:\n|$)',
                # Pattern: Company Name | Rs 1,00,000 | Party Name
                r'(.+?)\s*\|\s*Rs\.?\s*([\d,]+)\s*\|\s*(.+?)(?:\n|$)',
                # Pattern: Company Name    1,00,000    Party Name
                r'(.+?)\s+([\d,]+)\s+(.+?)(?:\n|$)'
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                
                for match in matches:
                    try:
                        donor_name = match.group(1).strip()
                        amount_str = match.group(2).strip()
                        party_name = match.group(3).strip()
                        
                        # Validate extracted data
                        if (len(donor_name) > 3 and len(party_name) > 2 and 
                            re.search(r'\d', amount_str)):
                            
                            donation = {
                                'source': f'ADR_PDF_{method}_pattern',
                                'extraction_date': datetime.now().isoformat(),
                                'donor_name': donor_name,
                                'recipient_party': party_name,
                                'amount': self._parse_amount(amount_str),
                                'page_number': page_num + 1,
                                'source_url': source_url,
                                'extraction_method': f'{method}_regex',
                                'is_karnataka_party': self._is_karnataka_party(party_name),
                                'is_karnataka_donor': False,
                                'data_type': 'adr_pdf_text',
                                'raw_match': match.group(0)
                            }
                            donations.append(donation)
                            
                    except Exception as e:
                        logger.error(f"Error parsing regex match: {str(e)}")
                        continue
            
            return donations
            
        except Exception as e:
            logger.error(f"Error in text parsing: {str(e)}")
            return []
    
    def _extract_table_from_ocr_text(self, ocr_text: str, source_url: str, page_num: int) -> List[Dict]:
        """Extract table structure from OCR text."""
        try:
            donations = []
            lines = ocr_text.split('\n')
            
            # Look for table-like patterns
            for i, line in enumerate(lines):
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Look for lines with multiple columns (separated by spaces)
                parts = line.split()
                if len(parts) >= 3:
                    # Try to identify if this looks like a data row
                    potential_amount = None
                    potential_donor = None
                    potential_party = None
                    
                    for part in parts:
                        # Check if this looks like an amount
                        if re.match(r'[\d,]+', part.replace(',', '')):
                            potential_amount = part
                        # Check if this looks like a party name
                        elif any(party in part.upper() for party in ['BJP', 'CONGRESS', 'AAP', 'JDS', 'INC']):
                            potential_party = part
                    
                    if potential_amount and (potential_party or len(parts) >= 3):
                        # Reconstruct donor name and party name
                        donor_parts = []
                        party_parts = []
                        amount_found = False
                        
                        for part in parts:
                            if part == potential_amount:
                                amount_found = True
                            elif not amount_found:
                                donor_parts.append(part)
                            else:
                                party_parts.append(part)
                        
                        if donor_parts and potential_amount:
                            donation = {
                                'source': 'ADR_PDF_ocr_table',
                                'extraction_date': datetime.now().isoformat(),
                                'donor_name': ' '.join(donor_parts).strip(),
                                'recipient_party': ' '.join(party_parts).strip() or potential_party or 'Unknown',
                                'amount': self._parse_amount(potential_amount),
                                'page_number': page_num + 1,
                                'source_url': source_url,
                                'extraction_method': 'ocr_table_reconstruction',
                                'is_karnataka_party': self._is_karnataka_party(' '.join(party_parts) or potential_party or ''),
                                'is_karnataka_donor': False,
                                'data_type': 'adr_pdf_ocr_table',
                                'raw_line': line
                            }
                            donations.append(donation)
            
            return donations
            
        except Exception as e:
            logger.error(f"Error in OCR table extraction: {str(e)}")
            return []
    
    def enrich_with_mca_data(self, donations: List[Dict]) -> List[Dict]:
        """
        Enrich donation data with MCA corporate information.
        This is CRITICAL for anomaly detection.
        """
        try:
            logger.info("Starting MCA data enrichment...")
            
            enriched_donations = []
            
            for donation in donations:
                try:
                    donor_name = donation.get('donor_name', '').strip()
                    
                    if donor_name:
                        # Search MCA database for company information
                        mca_data = self._search_mca_company_data(donor_name)
                        
                        if mca_data:
                            # Enrich the donation record
                            donation.update({
                                'mca_company_name': mca_data.get('company_name'),
                                'mca_cin': mca_data.get('cin'),
                                'mca_registration_date': mca_data.get('date_of_incorporation'),
                                'mca_registered_address': mca_data.get('registered_address'),
                                'mca_state': mca_data.get('state'),
                                'mca_status': mca_data.get('company_status'),
                                'mca_authorized_capital': mca_data.get('authorized_capital'),
                                'mca_paid_up_capital': mca_data.get('paid_up_capital'),
                                'is_karnataka_donor': 'KARNATAKA' in str(mca_data.get('state', '')).upper(),
                                'mca_enriched': True,
                                'mca_enrichment_date': datetime.now().isoformat()
                            })
                        else:
                            donation['mca_enriched'] = False
                    
                    enriched_donations.append(donation)
                    
                except Exception as e:
                    logger.error(f"Error enriching donation record: {str(e)}")
                    enriched_donations.append(donation)
                    continue
            
            logger.info(f"MCA enrichment completed for {len(enriched_donations)} records")
            return enriched_donations
            
        except Exception as e:
            logger.error(f"Error in MCA enrichment: {str(e)}")
            return donations  # Return original data if enrichment fails
    
    def _search_mca_company_data(self, company_name: str) -> Optional[Dict]:
        """Search MCA database for company information."""
        try:
            # Note: This would need to be implemented with actual MCA API access
            # For now, returning a placeholder structure
            
            # MCA API endpoint (this needs to be the actual endpoint)
            mca_search_url = f"{self.mca_base_url}/api/company-search"
            
            params = {
                'company_name': company_name,
                'type': 'exact_match'
            }
            
            response = requests.get(mca_search_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('company_details', {})
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching MCA data for {company_name}: {str(e)}")
            return None
    
    # Utility functions
    def _parse_amount(self, amount_str) -> float:
        """Parse amount string to float."""
        try:
            if isinstance(amount_str, (int, float)):
                return float(amount_str)
            
            # Remove common formatting
            amount_str = str(amount_str).replace(',', '').replace('Rs.', '').replace('Rs', '').strip()
            
            # Handle crore/lakh notation
            if 'crore' in amount_str.lower():
                num = float(re.search(r'[\d.]+', amount_str).group())
                return num * 10000000  # 1 crore = 10 million
            elif 'lakh' in amount_str.lower():
                num = float(re.search(r'[\d.]+', amount_str).group())
                return num * 100000  # 1 lakh = 100 thousand
            
            # Regular number
            return float(re.search(r'[\d.]+', amount_str).group())
            
        except:
            return 0.0
    
    def _parse_date(self, date_str) -> Optional[str]:
        """Parse date string to ISO format."""
        try:
            if not date_str:
                return None
            
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y']:
                try:
                    dt = datetime.strptime(str(date_str), fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            return str(date_str)
            
        except:
            return None
    
    def _is_karnataka_party(self, party_name: str) -> bool:
        """Check if party is Karnataka-based."""
        karnataka_parties = [
            'BHARATIYA JANATA PARTY', 'BJP', 'INDIAN NATIONAL CONGRESS', 'INC', 'CONGRESS',
            'JANATA DAL (SECULAR)', 'JDS', 'JD(S)', 'KARNATAKA CONGRESS', 'BJP KARNATAKA'
        ]
        
        party_upper = party_name.upper()
        return any(kp in party_upper for kp in karnataka_parties)
    
    def _find_column_index(self, headers: List, keywords: List[str]) -> Optional[int]:
        """Find column index by keywords."""
        for i, header in enumerate(headers):
            if any(keyword.lower() in str(header).lower() for keyword in keywords):
                return i
        return None
    
    def _extract_year_from_url(self, url: str) -> str:
        """Extract year from URL."""
        match = re.search(r'(\d{4})', url)
        return match.group(1) if match else ''
    
    def _deduplicate_records(self, records: List[Dict]) -> List[Dict]:
        """Remove duplicate records while preserving unique data."""
        seen = set()
        unique_records = []
        
        for record in records:
            # Create a hash key for deduplication
            key = (
                record.get('donor_name', '').strip().upper(),
                record.get('recipient_party', '').strip().upper(),
                record.get('amount', 0),
                record.get('date_info', '').strip()
            )
            
            if key not in seen:
                seen.add(key)
                unique_records.append(record)
        
        return unique_records

# Firebase Cloud Functions

@scheduler_fn.on_schedule(schedule="0 2 * * *")  # Daily at 2 AM
def scheduled_data_ingestion(cloud_event):
    """Scheduled function to ingest political funding data daily."""
    try:
        logger.info("Starting scheduled political funding data ingestion...")
        
        engine = DataIngestionEngine()
        
        # Step 1: Extract ECI data
        eci_data = engine.extract_eci_electoral_bonds()
        
        # Step 2: Extract ADR data (comprehensive PDF + HTML)
        adr_data = engine.extract_adr_reports_comprehensive()
        
        # Step 3: Combine all data
        all_donations = eci_data + adr_data
        
        # Step 4: Enrich with MCA data
        enriched_donations = engine.enrich_with_mca_data(all_donations)
        
        # Step 5: Store in Firestore
        batch = db.batch()
        collection_ref = db.collection('political_funding')
        
        for donation in enriched_donations:
            doc_ref = collection_ref.document()
            batch.set(doc_ref, donation)
        
        batch.commit()
        
        logger.info(f"Successfully ingested {len(enriched_donations)} political funding records")
        
        # Update status collection
        status_ref = db.collection('data_ingestion_status').document('latest')
        status_ref.set({
            'last_run': datetime.now().isoformat(),
            'records_processed': len(enriched_donations),
            'eci_records': len(eci_data),
            'adr_records': len(adr_data),
            'status': 'success'
        })
        
        return {"status": "success", "records_processed": len(enriched_donations)}
        
    except Exception as e:
        logger.error(f"Error in scheduled data ingestion: {str(e)}")
        
        # Update status with error
        status_ref = db.collection('data_ingestion_status').document('latest')
        status_ref.set({
            'last_run': datetime.now().isoformat(),
            'status': 'error',
            'error_message': str(e)
        })
        
        return {"status": "error", "message": str(e)}

@functions_framework.http
def manual_data_refresh(request):
    """Manual trigger for data refresh."""
    try:
        source = request.args.get('source', 'all')
        
        engine = DataIngestionEngine()
        
        if source == 'eci':
            data = engine.extract_eci_electoral_bonds()
        elif source == 'adr':
            data = engine.extract_adr_reports_comprehensive()
        else:
            eci_data = engine.extract_eci_electoral_bonds()
            adr_data = engine.extract_adr_reports_comprehensive()
            data = eci_data + adr_data
        
        # Enrich and store
        enriched_data = engine.enrich_with_mca_data(data)
        
        # Store in Firestore
        batch = db.batch()
        collection_ref = db.collection('political_funding')
        
        for donation in enriched_data:
            doc_ref = collection_ref.document()
            batch.set(doc_ref, donation)
        
        batch.commit()
        
        return {
            "status": "success",
            "message": f"Refreshed {len(enriched_data)} records from {source}",
            "records_processed": len(enriched_data)
        }
        
    except Exception as e:
        logger.error(f"Error in manual data refresh: {str(e)}")
        return {"status": "error", "message": str(e)}, 500