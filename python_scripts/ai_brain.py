#!/usr/bin/env python3
"""
AI Brain for Janata Audit Bengaluru
Detects anomalies and generates red flags
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from collections import defaultdict

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_config import get_firestore_client

class AIBrain:
    """AI system for detecting anomalies in civic projects and donations"""
    
    def __init__(self):
        self.db = get_firestore_client()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ai_brain.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def fetch_projects_data(self) -> pd.DataFrame:
        """Fetch projects data from Firestore"""
        try:
            projects_ref = self.db.collection('projects')
            projects_docs = projects_ref.get()
            
            projects_data = []
            for doc in projects_docs:
                project_data = doc.to_dict()
                project_data['id'] = doc.id
                projects_data.append(project_data)
            
            return pd.DataFrame(projects_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching projects data: {str(e)}")
            return pd.DataFrame()
    
    def fetch_donations_data(self) -> pd.DataFrame:
        """Fetch donations data from Firestore"""
        try:
            donations_ref = self.db.collection('politicalDonations')
            donations_docs = donations_ref.get()
            
            donations_data = []
            for doc in donations_docs:
                donation_data = doc.to_dict()
                donation_data['id'] = doc.id
                donations_data.append(donation_data)
            
            return pd.DataFrame(donations_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching donations data: {str(e)}")
            return pd.DataFrame()
    
    def detect_budget_anomalies(self, projects_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect budget-related anomalies"""
        anomalies = []
        
        if projects_df.empty:
            return anomalies
        
        try:
            # Convert budget to numeric
            projects_df['budget_numeric'] = projects_df['budget'].apply(self.extract_budget_numeric)
            
            # Filter out zero budgets
            valid_budgets = projects_df[projects_df['budget_numeric'] > 0]
            
            if len(valid_budgets) < 2:
                return anomalies
            
            # Calculate budget statistics by department
            dept_stats = valid_budgets.groupby('department')['budget_numeric'].agg(['mean', 'std', 'count'])
            
            for dept, stats in dept_stats.iterrows():
                if stats['count'] < 3:  # Need at least 3 projects for meaningful stats
                    continue
                
                # Find outliers (budget > mean + 2*std)
                threshold = stats['mean'] + 2 * stats['std']
                outliers = valid_budgets[
                    (valid_budgets['department'] == dept) & 
                    (valid_budgets['budget_numeric'] > threshold)
                ]
                
                for _, project in outliers.iterrows():
                    anomaly = {
                        'description': f"Unusually high budget for {dept} project: ₹{project['budget_numeric']:,.0f} (avg: ₹{stats['mean']:,.0f})",
                        'flagType': 'budget_anomaly',
                        'linkedProjectIds': [project['id']],
                        'linkedDonationIds': [],
                        'severity': 'high' if project['budget_numeric'] > stats['mean'] + 3 * stats['std'] else 'medium',
                        'detectedAt': datetime.now()
                    }
                    anomalies.append(anomaly)
            
        except Exception as e:
            self.logger.error(f"Error detecting budget anomalies: {str(e)}")
        
        return anomalies
    
    def detect_timing_anomalies(self, projects_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect timing-related anomalies"""
        anomalies = []
        
        if projects_df.empty:
            return anomalies
        
        try:
            # Convert dates
            projects_df['start_date'] = pd.to_datetime(projects_df['startDate'], errors='coerce')
            projects_df['end_date'] = pd.to_datetime(projects_df['endDate'], errors='coerce')
            projects_df['actual_end_date'] = pd.to_datetime(projects_df['actualCompletionDate'], errors='coerce')
            
            # Filter valid projects
            valid_projects = projects_df.dropna(subset=['start_date', 'end_date'])
            
            if len(valid_projects) < 2:
                return anomalies
            
            # Calculate project duration
            valid_projects['planned_duration'] = (valid_projects['end_date'] - valid_projects['start_date']).dt.days
            
            # Find extremely short or long projects
            duration_stats = valid_projects['planned_duration'].describe()
            
            # Short projects (less than 1st percentile)
            short_threshold = duration_stats['25%'] * 0.5  # Less than half of 25th percentile
            short_projects = valid_projects[valid_projects['planned_duration'] < short_threshold]
            
            for _, project in short_projects.iterrows():
                anomaly = {
                    'description': f"Unusually short project duration: {project['planned_duration']} days for {project['projectName']}",
                    'flagType': 'timing_anomaly',
                    'linkedProjectIds': [project['id']],
                    'linkedDonationIds': [],
                    'severity': 'medium',
                    'detectedAt': datetime.now()
                }
                anomalies.append(anomaly)
            
            # Long projects (more than 3rd quartile + 1.5*IQR)
            q75 = duration_stats['75%']
            q25 = duration_stats['25%']
            iqr = q75 - q25
            long_threshold = q75 + 1.5 * iqr
            
            long_projects = valid_projects[valid_projects['planned_duration'] > long_threshold]
            
            for _, project in long_projects.iterrows():
                anomaly = {
                    'description': f"Unusually long project duration: {project['planned_duration']} days for {project['projectName']}",
                    'flagType': 'timing_anomaly',
                    'linkedProjectIds': [project['id']],
                    'linkedDonationIds': [],
                    'severity': 'medium',
                    'detectedAt': datetime.now()
                }
                anomalies.append(anomaly)
            
        except Exception as e:
            self.logger.error(f"Error detecting timing anomalies: {str(e)}")
        
        return anomalies
    
    def detect_contractor_anomalies(self, projects_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect contractor-related anomalies"""
        anomalies = []
        
        if projects_df.empty:
            return anomalies
        
        try:
            # Filter projects with contractor information
            contractor_projects = projects_df[projects_df['contractorName'].notna()]
            
            if len(contractor_projects) < 2:
                return anomalies
            
            # Count projects per contractor
            contractor_counts = contractor_projects['contractorName'].value_counts()
            
            # Find contractors with unusually many projects
            mean_projects = contractor_counts.mean()
            std_projects = contractor_counts.std()
            
            if std_projects > 0:
                threshold = mean_projects + 2 * std_projects
                frequent_contractors = contractor_counts[contractor_counts > threshold]
                
                for contractor, count in frequent_contractors.items():
                    contractor_projects_list = contractor_projects[
                        contractor_projects['contractorName'] == contractor
                    ]
                    
                    anomaly = {
                        'description': f"Contractor {contractor} has unusually many projects: {count} (avg: {mean_projects:.1f})",
                        'flagType': 'contractor_anomaly',
                        'linkedProjectIds': contractor_projects_list['id'].tolist(),
                        'linkedDonationIds': [],
                        'severity': 'high' if count > mean_projects + 3 * std_projects else 'medium',
                        'detectedAt': datetime.now()
                    }
                    anomalies.append(anomaly)
            
        except Exception as e:
            self.logger.error(f"Error detecting contractor anomalies: {str(e)}")
        
        return anomalies
    
    def detect_donation_project_correlations(self, projects_df: pd.DataFrame, donations_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect correlations between donations and projects"""
        anomalies = []
        
        if projects_df.empty or donations_df.empty:
            return anomalies
        
        try:
            # Group donations by party
            party_donations = donations_df.groupby('politicalPartyName')['amount'].sum().sort_values(ascending=False)
            
            # Group projects by department
            dept_projects = projects_df.groupby('department').size().sort_values(ascending=False)
            
            # Look for patterns (this is a simplified correlation check)
            # In a real implementation, you'd do more sophisticated analysis
            
            for party, total_donation in party_donations.head(5).items():
                # Check if there are any projects that might be related
                # This is a placeholder for more sophisticated correlation analysis
                if total_donation > 1000000:  # More than 10 lakh
                    anomaly = {
                        'description': f"High-value donations from {party}: ₹{total_donation:,.0f} - investigate potential project correlations",
                        'flagType': 'donation_correlation',
                        'linkedProjectIds': [],
                        'linkedDonationIds': donations_df[donations_df['politicalPartyName'] == party]['id'].tolist(),
                        'severity': 'medium',
                        'detectedAt': datetime.now()
                    }
                    anomalies.append(anomaly)
            
        except Exception as e:
            self.logger.error(f"Error detecting donation-project correlations: {str(e)}")
        
        return anomalies
    
    def extract_budget_numeric(self, budget_str):
        """Extract numeric value from budget string"""
        if pd.isna(budget_str) or not budget_str:
            return 0
        
        import re
        # Remove common text and symbols
        budget_str = str(budget_str).replace(',', '').replace('₹', '').replace('Rs.', '')
        
        # Handle Lakh and Crore
        if 'Lakh' in budget_str or 'L' in budget_str:
            budget_str = budget_str.replace('Lakh', '').replace('L', '')
            multiplier = 100000
        elif 'Crore' in budget_str or 'Cr' in budget_str:
            budget_str = budget_str.replace('Crore', '').replace('Cr', '')
            multiplier = 10000000
        else:
            multiplier = 1
        
        # Extract numbers
        numbers = re.findall(r'[\d.]+', budget_str)
        if numbers:
            try:
                return float(numbers[0]) * multiplier
            except ValueError:
                return 0
        return 0
    
    def save_anomalies_to_firestore(self, anomalies: List[Dict[str, Any]]):
        """Save detected anomalies to Firestore"""
        if not anomalies:
            return
        
        try:
            batch = self.db.batch()
            anomalies_ref = self.db.collection('aiRedFlags')
            
            for anomaly in anomalies:
                # Add metadata
                anomaly['detectedAt'] = datetime.now()
                anomaly['status'] = 'active'
                
                # Create document reference
                doc_ref = anomalies_ref.document()
                batch.set(doc_ref, anomaly)
            
            # Commit batch
            batch.commit()
            self.logger.info(f"Saved {len(anomalies)} anomalies to Firestore")
            
        except Exception as e:
            self.logger.error(f"Error saving anomalies to Firestore: {str(e)}")
    
    def find_suspicious_connections(self):
        """Main method to find suspicious connections and anomalies"""
        self.logger.info("Starting AI anomaly detection...")
        
        try:
            # Fetch data
            projects_df = self.fetch_projects_data()
            donations_df = self.fetch_donations_data()
            
            self.logger.info(f"Loaded {len(projects_df)} projects and {len(donations_df)} donations")
            
            # Detect various types of anomalies
            all_anomalies = []
            
            # Budget anomalies
            budget_anomalies = self.detect_budget_anomalies(projects_df)
            all_anomalies.extend(budget_anomalies)
            self.logger.info(f"Detected {len(budget_anomalies)} budget anomalies")
            
            # Timing anomalies
            timing_anomalies = self.detect_timing_anomalies(projects_df)
            all_anomalies.extend(timing_anomalies)
            self.logger.info(f"Detected {len(timing_anomalies)} timing anomalies")
            
            # Contractor anomalies
            contractor_anomalies = self.detect_contractor_anomalies(projects_df)
            all_anomalies.extend(contractor_anomalies)
            self.logger.info(f"Detected {len(contractor_anomalies)} contractor anomalies")
            
            # Donation-project correlations
            correlation_anomalies = self.detect_donation_project_correlations(projects_df, donations_df)
            all_anomalies.extend(correlation_anomalies)
            self.logger.info(f"Detected {len(correlation_anomalies)} correlation anomalies")
            
            # Save anomalies to Firestore
            self.save_anomalies_to_firestore(all_anomalies)
            
            self.logger.info(f"AI analysis completed. Total anomalies detected: {len(all_anomalies)}")
            
            return all_anomalies
            
        except Exception as e:
            self.logger.error(f"Error in AI analysis: {str(e)}")
            return []

def main():
    """Main function"""
    ai_brain = AIBrain()
    
    try:
        anomalies = ai_brain.find_suspicious_connections()
        print(f"AI analysis completed successfully!")
        print(f"Total anomalies detected: {len(anomalies)}")
        
        # Print summary
        anomaly_types = {}
        for anomaly in anomalies:
            flag_type = anomaly['flagType']
            anomaly_types[flag_type] = anomaly_types.get(flag_type, 0) + 1
        
        print("\nAnomaly Summary:")
        for flag_type, count in anomaly_types.items():
            print(f"  {flag_type}: {count}")
        
    except Exception as e:
        print(f"Error in AI analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
