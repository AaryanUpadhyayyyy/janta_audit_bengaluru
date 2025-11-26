# Political Funding Anomaly Detection Engine
# This module identifies suspicious patterns and red flags in political funding data

import functions_framework
from firebase_functions import firestore_fn, scheduler_fn
from google.cloud import firestore
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Optional, Tuple
import json
from collections import defaultdict
import re

# Initialize Firestore client
db = firestore.Client()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetectionEngine:
    """
    Advanced anomaly detection engine for political funding data.
    Identifies suspicious patterns, red flags, and potential corruption indicators.
    """
    
    def __init__(self):
        self.anomaly_types = {
            'excessive_donation': 'Donation exceeds company profits',
            'shell_company': 'Multiple companies with same address/directors',
            'timing_suspicious': 'Large donations before/after contracts',
            'new_company_large_donation': 'Large donation from newly incorporated company',
            'round_number_pattern': 'Suspicious round number donations',
            'address_clustering': 'Multiple donors from same address',
            'dormant_company_activity': 'Donation from dormant company',
            'disproportionate_donation': 'Donation disproportionate to company size'
        }
        
        # Thresholds for anomaly detection
        self.thresholds = {
            'profit_ratio_threshold': 0.5,  # Donation > 50% of profit
            'new_company_days': 365,  # Company incorporated within 1 year
            'large_donation_threshold': 1000000,  # Rs. 10 Lakh
            'round_number_threshold': 0.8,  # 80% of donations are round numbers
            'address_cluster_min': 3  # Minimum companies at same address
        }
    
    def analyze_all_funding_data(self) -> List[Dict]:
        """
        Comprehensive analysis of all political funding data.
        Returns list of detected anomalies and red flags.
        """
        try:
            logger.info("Starting comprehensive funding anomaly analysis...")
            
            # Fetch all funding data
            funding_data = self._fetch_funding_data()
            
            if not funding_data:
                logger.warning("No funding data found for analysis")
                return []
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(funding_data)
            
            # Run all anomaly detection methods
            all_anomalies = []
            
            # 1. Excessive donation analysis
            excessive_anomalies = self._detect_excessive_donations(df)
            all_anomalies.extend(excessive_anomalies)
            
            # 2. Shell company detection
            shell_anomalies = self._detect_shell_companies(df)
            all_anomalies.extend(shell_anomalies)
            
            # 3. Timing-based suspicious patterns
            timing_anomalies = self._detect_suspicious_timing(df)
            all_anomalies.extend(timing_anomalies)
            
            # 4. New company large donations
            new_company_anomalies = self._detect_new_company_large_donations(df)
            all_anomalies.extend(new_company_anomalies)
            
            # 5. Round number pattern analysis
            round_number_anomalies = self._detect_round_number_patterns(df)
            all_anomalies.extend(round_number_anomalies)
            
            # 6. Address clustering analysis
            address_anomalies = self._detect_address_clustering(df)
            all_anomalies.extend(address_anomalies)
            
            # 7. Dormant company activity
            dormant_anomalies = self._detect_dormant_company_activity(df)
            all_anomalies.extend(dormant_anomalies)
            
            # 8. Disproportionate donation analysis
            disproportionate_anomalies = self._detect_disproportionate_donations(df)
            all_anomalies.extend(disproportionate_anomalies)
            
            logger.info(f"Detected {len(all_anomalies)} anomalies across all categories")
            
            return all_anomalies
            
        except Exception as e:
            logger.error(f"Error in anomaly analysis: {str(e)}")
            return []
    
    def _fetch_funding_data(self) -> List[Dict]:
        """Fetch all political funding data from Firestore."""
        try:
            docs = db.collection('political_funding').stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Error fetching funding data: {str(e)}")
            return []
    
    def _detect_excessive_donations(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect donations that exceed company profits.
        This is a major red flag for potential money laundering.
        """
        try:
            anomalies = []
            
            # Filter records with MCA financial data
            financial_data = df[df['mca_enriched'] == True].copy()
            
            if financial_data.empty:
                return anomalies
            
            # Convert amount and financial data to numeric
            financial_data['amount'] = pd.to_numeric(financial_data['amount'], errors='coerce')
            financial_data['mca_authorized_capital'] = pd.to_numeric(
                financial_data['mca_authorized_capital'], errors='coerce'
            )
            financial_data['mca_paid_up_capital'] = pd.to_numeric(
                financial_data['mca_paid_up_capital'], errors='coerce'
            )
            
            for _, row in financial_data.iterrows():
                try:
                    donation_amount = row['amount']
                    authorized_capital = row.get('mca_authorized_capital', 0)
                    paid_up_capital = row.get('mca_paid_up_capital', 0)
                    
                    # Check if donation exceeds reasonable threshold relative to capital
                    capital_threshold = max(authorized_capital, paid_up_capital) * self.thresholds['profit_ratio_threshold']
                    
                    if donation_amount > capital_threshold and capital_threshold > 0:
                        anomaly = {
                            'anomaly_type': 'excessive_donation',
                            'severity': 'HIGH',
                            'donor_name': row['donor_name'],
                            'recipient_party': row['recipient_party'],
                            'donation_amount': donation_amount,
                            'company_capital': max(authorized_capital, paid_up_capital),
                            'ratio': donation_amount / max(authorized_capital, paid_up_capital, 1),
                            'description': f"Donation of ₹{donation_amount:,.0f} exceeds {self.thresholds['profit_ratio_threshold']*100}% of company capital (₹{capital_threshold:,.0f})",
                            'detection_date': datetime.now().isoformat(),
                            'source_data': row.to_dict(),
                            'risk_score': min(100, (donation_amount / max(capital_threshold, 1)) * 50)
                        }
                        anomalies.append(anomaly)
                        
                except Exception as e:
                    logger.error(f"Error processing excessive donation for {row.get('donor_name')}: {str(e)}")
                    continue
            
            logger.info(f"Detected {len(anomalies)} excessive donation anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in excessive donation detection: {str(e)}")
            return []
    
    def _detect_shell_companies(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect potential shell companies based on address clustering.
        Multiple companies at same address making donations is suspicious.
        """
        try:
            anomalies = []
            
            # Group by registered address
            address_groups = df.groupby('mca_registered_address')
            
            for address, group in address_groups:
                if len(group) >= self.thresholds['address_cluster_min'] and pd.notna(address):
                    # Calculate total donations from this address
                    total_donations = group['amount'].sum()
                    companies = group['donor_name'].unique()
                    recipients = group['recipient_party'].unique()
                    
                    anomaly = {
                        'anomaly_type': 'shell_company',
                        'severity': 'HIGH' if len(companies) >= 5 else 'MEDIUM',
                        'address': address,
                        'company_count': len(companies),
                        'companies': companies.tolist(),
                        'total_donations': total_donations,
                        'recipients': recipients.tolist(),
                        'description': f"{len(companies)} companies at same address donated total ₹{total_donations:,.0f}",
                        'detection_date': datetime.now().isoformat(),
                        'risk_score': min(100, len(companies) * 15),
                        'source_data': group.to_dict('records')
                    }
                    anomalies.append(anomaly)
            
            logger.info(f"Detected {len(anomalies)} shell company anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in shell company detection: {str(e)}")
            return []
    
    def _detect_suspicious_timing(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect suspicious timing patterns in donations.
        Large donations close to election dates or contract awards.
        """
        try:
            anomalies = []
            
            # Key election dates for Karnataka
            election_dates = [
                datetime(2023, 5, 10),  # Karnataka Assembly Elections 2023
                datetime(2024, 4, 26),  # Lok Sabha Elections 2024
            ]
            
            # Convert date columns
            for date_col in ['date_of_purchase', 'date_of_encashment']:
                if date_col in df.columns:
                    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            
            for _, row in df.iterrows():
                try:
                    donation_date = None
                    
                    # Try to get donation date
                    for date_col in ['date_of_purchase', 'date_of_encashment']:
                        if pd.notna(row.get(date_col)):
                            donation_date = row[date_col]
                            break
                    
                    if donation_date and row['amount'] > self.thresholds['large_donation_threshold']:
                        # Check proximity to election dates
                        for election_date in election_dates:
                            days_difference = abs((donation_date - election_date).days)
                            
                            if days_difference <= 90:  # Within 3 months of election
                                anomaly = {
                                    'anomaly_type': 'timing_suspicious',
                                    'severity': 'HIGH' if days_difference <= 30 else 'MEDIUM',
                                    'donor_name': row['donor_name'],
                                    'recipient_party': row['recipient_party'],
                                    'donation_amount': row['amount'],
                                    'donation_date': donation_date.isoformat(),
                                    'election_date': election_date.isoformat(),
                                    'days_to_election': days_difference,
                                    'description': f"Large donation of ₹{row['amount']:,.0f} made {days_difference} days before election",
                                    'detection_date': datetime.now().isoformat(),
                                    'risk_score': max(30, 100 - days_difference),
                                    'source_data': row.to_dict()
                                }
                                anomalies.append(anomaly)
                                break
                                
                except Exception as e:
                    logger.error(f"Error processing timing for {row.get('donor_name')}: {str(e)}")
                    continue
            
            logger.info(f"Detected {len(anomalies)} suspicious timing anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in suspicious timing detection: {str(e)}")
            return []
    
    def _detect_new_company_large_donations(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect large donations from newly incorporated companies.
        New companies making large donations is highly suspicious.
        """
        try:
            anomalies = []
            
            # Convert registration date
            df['mca_registration_date'] = pd.to_datetime(df['mca_registration_date'], errors='coerce')
            
            for _, row in df.iterrows():
                try:
                    if (pd.notna(row.get('mca_registration_date')) and 
                        row['amount'] > self.thresholds['large_donation_threshold']):
                        
                        # Calculate company age at time of donation
                        registration_date = row['mca_registration_date']
                        
                        # Try to get donation date
                        donation_date = None
                        for date_col in ['date_of_purchase', 'date_of_encashment']:
                            if pd.notna(row.get(date_col)):
                                donation_date = pd.to_datetime(row[date_col])
                                break
                        
                        if not donation_date:
                            donation_date = datetime.now()  # Use current date as fallback
                        
                        company_age_days = (donation_date - registration_date).days
                        
                        if company_age_days <= self.thresholds['new_company_days']:
                            anomaly = {
                                'anomaly_type': 'new_company_large_donation',
                                'severity': 'HIGH' if company_age_days <= 180 else 'MEDIUM',
                                'donor_name': row['donor_name'],
                                'recipient_party': row['recipient_party'],
                                'donation_amount': row['amount'],
                                'registration_date': registration_date.isoformat(),
                                'donation_date': donation_date.isoformat(),
                                'company_age_days': company_age_days,
                                'description': f"Company incorporated {company_age_days} days ago donated ₹{row['amount']:,.0f}",
                                'detection_date': datetime.now().isoformat(),
                                'risk_score': max(60, 100 - (company_age_days / 10)),
                                'source_data': row.to_dict()
                            }
                            anomalies.append(anomaly)
                            
                except Exception as e:
                    logger.error(f"Error processing new company for {row.get('donor_name')}: {str(e)}")
                    continue
            
            logger.info(f"Detected {len(anomalies)} new company large donation anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in new company detection: {str(e)}")
            return []
    
    def _detect_round_number_patterns(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect suspicious round number patterns in donations.
        Too many round number donations may indicate artificial transactions.
        """
        try:
            anomalies = []
            
            # Group by donor to analyze their donation patterns
            donor_groups = df.groupby('donor_name')
            
            for donor_name, group in donor_groups:
                if len(group) >= 3:  # Need multiple donations to establish pattern
                    amounts = group['amount'].values
                    
                    # Count round numbers (ending in 00000, 000000, etc.)
                    round_numbers = sum(1 for amount in amounts 
                                      if amount % 100000 == 0 and amount > 0)
                    
                    round_ratio = round_numbers / len(amounts)
                    
                    if round_ratio >= self.thresholds['round_number_threshold']:
                        total_donations = amounts.sum()
                        recipients = group['recipient_party'].unique()
                        
                        anomaly = {
                            'anomaly_type': 'round_number_pattern',
                            'severity': 'MEDIUM',
                            'donor_name': donor_name,
                            'total_donations': len(amounts),
                            'round_number_donations': round_numbers,
                            'round_number_ratio': round_ratio,
                            'total_amount': total_donations,
                            'recipients': recipients.tolist(),
                            'description': f"{round_numbers}/{len(amounts)} donations are round numbers ({round_ratio*100:.1f}%)",
                            'detection_date': datetime.now().isoformat(),
                            'risk_score': round_ratio * 50,
                            'source_data': group.to_dict('records')
                        }
                        anomalies.append(anomaly)
            
            logger.info(f"Detected {len(anomalies)} round number pattern anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in round number pattern detection: {str(e)}")
            return []
    
    def _detect_address_clustering(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect address clustering patterns beyond shell companies.
        Multiple unrelated donations from same location.
        """
        try:
            anomalies = []
            
            # Extract city/area from addresses
            df['address_clean'] = df['mca_registered_address'].fillna('').str.upper()
            
            # Group by cleaned address
            address_groups = df.groupby('address_clean')
            
            for address, group in address_groups:
                if len(group) >= self.thresholds['address_cluster_min'] and address:
                    # Check if donations go to different parties
                    recipients = group['recipient_party'].unique()
                    donors = group['donor_name'].unique()
                    
                    if len(recipients) > 1 and len(donors) >= 3:
                        total_amount = group['amount'].sum()
                        
                        anomaly = {
                            'anomaly_type': 'address_clustering',
                            'severity': 'MEDIUM',
                            'address': address,
                            'donor_count': len(donors),
                            'recipient_count': len(recipients),
                            'total_amount': total_amount,
                            'donors': donors.tolist(),
                            'recipients': recipients.tolist(),
                            'description': f"{len(donors)} donors from same address donated to {len(recipients)} different parties",
                            'detection_date': datetime.now().isoformat(),
                            'risk_score': min(60, len(donors) * 10),
                            'source_data': group.to_dict('records')
                        }
                        anomalies.append(anomaly)
            
            logger.info(f"Detected {len(anomalies)} address clustering anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in address clustering detection: {str(e)}")
            return []
    
    def _detect_dormant_company_activity(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect donations from companies that appear to be dormant.
        Based on MCA status and activity patterns.
        """
        try:
            anomalies = []
            
            dormant_indicators = ['DORMANT', 'INACTIVE', 'STRIKE OFF', 'DISSOLVED']
            
            for _, row in df.iterrows():
                try:
                    company_status = str(row.get('mca_status', '')).upper()
                    
                    if any(indicator in company_status for indicator in dormant_indicators):
                        if row['amount'] > 0:
                            anomaly = {
                                'anomaly_type': 'dormant_company_activity',
                                'severity': 'HIGH',
                                'donor_name': row['donor_name'],
                                'recipient_party': row['recipient_party'],
                                'donation_amount': row['amount'],
                                'company_status': company_status,
                                'description': f"Donation of ₹{row['amount']:,.0f} from dormant/inactive company",
                                'detection_date': datetime.now().isoformat(),
                                'risk_score': 85,
                                'source_data': row.to_dict()
                            }
                            anomalies.append(anomaly)
                            
                except Exception as e:
                    logger.error(f"Error processing dormant company for {row.get('donor_name')}: {str(e)}")
                    continue
            
            logger.info(f"Detected {len(anomalies)} dormant company anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in dormant company detection: {str(e)}")
            return []
    
    def _detect_disproportionate_donations(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect donations that are disproportionate to company size/capital.
        """
        try:
            anomalies = []
            
            for _, row in df.iterrows():
                try:
                    if (pd.notna(row.get('mca_paid_up_capital')) and 
                        row.get('mca_paid_up_capital', 0) > 0):
                        
                        paid_up_capital = float(row['mca_paid_up_capital'])
                        donation_amount = float(row['amount'])
                        
                        # If donation is more than 10 times the paid-up capital
                        if donation_amount > (paid_up_capital * 10):
                            ratio = donation_amount / paid_up_capital
                            
                            anomaly = {
                                'anomaly_type': 'disproportionate_donation',
                                'severity': 'HIGH' if ratio > 50 else 'MEDIUM',
                                'donor_name': row['donor_name'],
                                'recipient_party': row['recipient_party'],
                                'donation_amount': donation_amount,
                                'paid_up_capital': paid_up_capital,
                                'ratio': ratio,
                                'description': f"Donation is {ratio:.1f}x the company's paid-up capital",
                                'detection_date': datetime.now().isoformat(),
                                'risk_score': min(100, ratio * 2),
                                'source_data': row.to_dict()
                            }
                            anomalies.append(anomaly)
                            
                except Exception as e:
                    logger.error(f"Error processing disproportionate donation for {row.get('donor_name')}: {str(e)}")
                    continue
            
            logger.info(f"Detected {len(anomalies)} disproportionate donation anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in disproportionate donation detection: {str(e)}")
            return []

# Firebase Cloud Functions

@scheduler_fn.on_schedule(schedule="0 6 * * *")  # Daily at 6 AM (after data ingestion)
def scheduled_anomaly_detection(cloud_event):
    """Scheduled function to run anomaly detection daily."""
    try:
        logger.info("Starting scheduled anomaly detection...")
        
        engine = AnomalyDetectionEngine()
        anomalies = engine.analyze_all_funding_data()
        
        if anomalies:
            # Store anomalies in Firestore
            batch = db.batch()
            collection_ref = db.collection('audit_reports')
            
            # Clear previous anomalies from today
            today = datetime.now().date().isoformat()
            existing_docs = collection_ref.where('detection_date', '>=', today).stream()
            for doc in existing_docs:
                batch.delete(doc.reference)
            
            # Add new anomalies
            for anomaly in anomalies:
                doc_ref = collection_ref.document()
                batch.set(doc_ref, anomaly)
            
            batch.commit()
            
            logger.info(f"Stored {len(anomalies)} anomalies in audit_reports collection")
        
        # Update analysis status
        status_ref = db.collection('anomaly_detection_status').document('latest')
        status_ref.set({
            'last_run': datetime.now().isoformat(),
            'anomalies_detected': len(anomalies),
            'status': 'success',
            'anomaly_breakdown': {
                anomaly_type: len([a for a in anomalies if a['anomaly_type'] == anomaly_type])
                for anomaly_type in set(a['anomaly_type'] for a in anomalies)
            }
        })
        
        return {"status": "success", "anomalies_detected": len(anomalies)}
        
    except Exception as e:
        logger.error(f"Error in scheduled anomaly detection: {str(e)}")
        
        status_ref = db.collection('anomaly_detection_status').document('latest')
        status_ref.set({
            'last_run': datetime.now().isoformat(),
            'status': 'error',
            'error_message': str(e)
        })
        
        return {"status": "error", "message": str(e)}

@functions_framework.http
def manual_anomaly_analysis(request):
    """Manual trigger for anomaly analysis."""
    try:
        engine = AnomalyDetectionEngine()
        anomalies = engine.analyze_all_funding_data()
        
        # Store in Firestore
        batch = db.batch()
        collection_ref = db.collection('audit_reports')
        
        for anomaly in anomalies:
            doc_ref = collection_ref.document()
            batch.set(doc_ref, anomaly)
        
        batch.commit()
        
        return {
            "status": "success",
            "message": f"Analyzed funding data and detected {len(anomalies)} anomalies",
            "anomalies_detected": len(anomalies),
            "anomaly_types": list(set(a['anomaly_type'] for a in anomalies))
        }
        
    except Exception as e:
        logger.error(f"Error in manual anomaly analysis: {str(e)}")
        return {"status": "error", "message": str(e)}, 500