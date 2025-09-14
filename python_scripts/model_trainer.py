#!/usr/bin/env python3
"""
ML Model Trainer for Janata Audit Bengaluru
Trains a RandomForest model to predict project delays
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_config import get_firestore_client

class ProjectDelayPredictor:
    """ML model for predicting project delays"""
    
    def __init__(self):
        self.db = get_firestore_client()
        self.model = None
        self.label_encoders = {}
        self.feature_columns = []
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('model_trainer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def fetch_training_data(self) -> pd.DataFrame:
        """Fetch completed projects data from Firestore for training"""
        try:
            # Get completed projects
            projects_ref = self.db.collection('projects')
            projects_docs = projects_ref.where('status', '==', 'Completed').get()
            
            projects_data = []
            for doc in projects_docs:
                project_data = doc.to_dict()
                project_data['id'] = doc.id
                projects_data.append(project_data)
            
            return pd.DataFrame(projects_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching training data: {str(e)}")
            return pd.DataFrame()
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess and clean the data"""
        if df.empty:
            return df
        
        self.logger.info(f"Starting preprocessing of {len(df)} projects")
        
        # Create a copy to avoid modifying original
        df_processed = df.copy()
        
        # Convert dates
        df_processed['start_date'] = pd.to_datetime(df_processed['startDate'], errors='coerce')
        df_processed['end_date'] = pd.to_datetime(df_processed['endDate'], errors='coerce')
        df_processed['actual_end_date'] = pd.to_datetime(df_processed['actualCompletionDate'], errors='coerce')
        
        # Calculate target variable: is_delayed
        df_processed['is_delayed'] = 0
        valid_dates = df_processed.dropna(subset=['end_date', 'actual_end_date'])
        df_processed.loc[valid_dates.index, 'is_delayed'] = (
            valid_dates['actual_end_date'] > valid_dates['end_date']
        ).astype(int)
        
        # Calculate planned duration in days
        df_processed['planned_duration_days'] = (
            df_processed['end_date'] - df_processed['start_date']
        ).dt.days
        
        # Extract budget as numeric
        df_processed['budget_numeric'] = df_processed['budget'].apply(self.extract_budget_numeric)
        
        # Handle missing values
        df_processed['budget_numeric'] = df_processed['budget_numeric'].fillna(0)
        df_processed['planned_duration_days'] = df_processed['planned_duration_days'].fillna(0)
        df_processed['department'] = df_processed['department'].fillna('Unknown')
        df_processed['contractorName'] = df_processed['contractorName'].fillna('Unknown')
        
        # Extract ward number
        df_processed['ward_number'] = df_processed['wardNumber'].apply(self.extract_ward_number)
        
        # Create month features
        df_processed['start_month'] = df_processed['start_date'].dt.month
        df_processed['start_year'] = df_processed['start_date'].dt.year
        
        self.logger.info(f"Preprocessing completed. {df_processed['is_delayed'].sum()} delayed projects out of {len(df_processed)}")
        
        return df_processed
    
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
    
    def extract_ward_number(self, ward_str):
        """Extract ward number from ward string"""
        if pd.isna(ward_str) or not ward_str:
            return 0
        
        import re
        ward_match = re.search(r'(\d+)', str(ward_str))
        if ward_match:
            return int(ward_match.group(1))
        return 0
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features for the model"""
        if df.empty:
            return df
        
        self.logger.info("Creating features for the model")
        
        # Select features
        feature_columns = [
            'budget_numeric',
            'planned_duration_days',
            'ward_number',
            'start_month',
            'start_year',
            'department',
            'contractorName'
        ]
        
        # Create feature dataframe
        features_df = df[feature_columns].copy()
        
        # One-hot encode categorical variables
        categorical_columns = ['department', 'contractorName']
        
        for col in categorical_columns:
            if col in features_df.columns:
                # Use label encoding for high cardinality categorical variables
                if features_df[col].nunique() > 50:  # High cardinality
                    le = LabelEncoder()
                    features_df[f'{col}_encoded'] = le.fit_transform(features_df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    # One-hot encoding for low cardinality
                    dummies = pd.get_dummies(features_df[col], prefix=col)
                    features_df = pd.concat([features_df, dummies], axis=1)
        
        # Remove original categorical columns
        features_df = features_df.drop(columns=categorical_columns, errors='ignore')
        
        # Store feature columns for later use
        self.feature_columns = features_df.columns.tolist()
        
        self.logger.info(f"Created {len(self.feature_columns)} features")
        
        return features_df
    
    def train_model(self, X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
        """Train the RandomForest model"""
        self.logger.info("Training RandomForest model")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train the model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.logger.info(f"Model training completed. Accuracy: {accuracy:.3f}")
        self.logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
        
        return model
    
    def save_model(self, model: RandomForestClassifier):
        """Save the trained model and encoders"""
        try:
            # Save the model
            model_path = 'delay_predictor.pkl'
            joblib.dump(model, model_path)
            self.logger.info(f"Model saved to {model_path}")
            
            # Save the encoders
            encoders_path = 'label_encoders.pkl'
            joblib.dump(self.label_encoders, encoders_path)
            self.logger.info(f"Encoders saved to {encoders_path}")
            
            # Save feature columns
            features_path = 'feature_columns.pkl'
            joblib.dump(self.feature_columns, features_path)
            self.logger.info(f"Feature columns saved to {features_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            raise
    
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            # Load the model
            model_path = 'delay_predictor.pkl'
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                self.logger.info(f"Model loaded from {model_path}")
            else:
                self.logger.warning(f"Model file {model_path} not found")
                return False
            
            # Load the encoders
            encoders_path = 'label_encoders.pkl'
            if os.path.exists(encoders_path):
                self.label_encoders = joblib.load(encoders_path)
                self.logger.info(f"Encoders loaded from {encoders_path}")
            else:
                self.logger.warning(f"Encoders file {encoders_path} not found")
                return False
            
            # Load feature columns
            features_path = 'feature_columns.pkl'
            if os.path.exists(features_path):
                self.feature_columns = joblib.load(features_path)
                self.logger.info(f"Feature columns loaded from {features_path}")
            else:
                self.logger.warning(f"Feature columns file {features_path} not found")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            return False
    
    def predict_delay_risk(self, project_data: Dict[str, Any]) -> str:
        """Predict delay risk for a single project"""
        if not self.model:
            if not self.load_model():
                return "Unknown"
        
        try:
            # Preprocess the project data
            df = pd.DataFrame([project_data])
            df_processed = self.preprocess_data(df)
            
            if df_processed.empty:
                return "Unknown"
            
            # Create features
            features_df = self.create_features(df_processed)
            
            # Ensure all required features are present
            for col in self.feature_columns:
                if col not in features_df.columns:
                    features_df[col] = 0
            
            # Select only the features used in training
            features_df = features_df[self.feature_columns]
            
            # Make prediction
            prediction = self.model.predict(features_df)[0]
            prediction_proba = self.model.predict_proba(features_df)[0]
            
            # Convert prediction to risk level
            if prediction == 1:
                if prediction_proba[1] > 0.8:
                    return "High"
                elif prediction_proba[1] > 0.6:
                    return "Medium"
                else:
                    return "Low"
            else:
                return "Low"
                
        except Exception as e:
            self.logger.error(f"Error predicting delay risk: {str(e)}")
            return "Unknown"
    
    def train_and_save_model(self):
        """Main method to train and save the model"""
        self.logger.info("Starting model training process")
        
        try:
            # Fetch training data
            df = self.fetch_training_data()
            
            if df.empty:
                self.logger.warning("No training data available")
                return False
            
            self.logger.info(f"Fetched {len(df)} completed projects for training")
            
            # Preprocess data
            df_processed = self.preprocess_data(df)
            
            if df_processed.empty:
                self.logger.warning("No valid data after preprocessing")
                return False
            
            # Check if we have enough delayed projects
            delayed_count = df_processed['is_delayed'].sum()
            if delayed_count < 5:
                self.logger.warning(f"Not enough delayed projects for training: {delayed_count}")
                return False
            
            # Create features
            features_df = self.create_features(df_processed)
            
            if features_df.empty:
                self.logger.warning("No features created")
                return False
            
            # Prepare target variable
            y = df_processed['is_delayed']
            
            # Train the model
            model = self.train_model(features_df, y)
            
            # Save the model
            self.save_model(model)
            
            self.logger.info("Model training completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in model training: {str(e)}")
            return False

def main():
    """Main function"""
    trainer = ProjectDelayPredictor()
    
    try:
        success = trainer.train_and_save_model()
        
        if success:
            print("Model training completed successfully!")
            print("Files created:")
            print("  - delay_predictor.pkl (trained model)")
            print("  - label_encoders.pkl (categorical encoders)")
            print("  - feature_columns.pkl (feature column names)")
        else:
            print("Model training failed. Check logs for details.")
            sys.exit(1)
        
    except Exception as e:
        print(f"Error in model training: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
