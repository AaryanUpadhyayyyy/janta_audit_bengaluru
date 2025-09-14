#!/usr/bin/env python3
"""
Satellite Inspector - Advanced AI Module for Janata Audit Bengaluru
Automated satellite imagery analysis using Google Earth Engine for project verification
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import ee
import firebase_admin
from firebase_admin import firestore
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SatelliteInspector:
    """Advanced satellite imagery analysis for project verification"""
    
    def __init__(self):
        self.setup_logging()
        self.initialize_services()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('satellite_inspector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_services(self):
        """Initialize Google Earth Engine and Firebase services"""
        try:
            # Initialize Google Earth Engine
            if not ee.data._initialized:
                # Try to initialize with service account
                service_account_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
                if os.path.exists(service_account_path):
                    credentials = ee.ServiceAccountCredentials(None, service_account_path)
                    ee.Initialize(credentials)
                    self.logger.info("Google Earth Engine initialized with service account")
                else:
                    # Initialize with default credentials
                    ee.Initialize()
                    self.logger.info("Google Earth Engine initialized with default credentials")
            
            # Initialize Firebase Admin (if not already initialized)
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            
            self.db = firestore.client()
            self.logger.info("Services initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing services: {str(e)}")
            raise
    
    def get_project_roi(self, geo_point: Dict[str, float], buffer_meters: int = 500) -> ee.Geometry:
        """Create Region of Interest around project location"""
        try:
            lat = geo_point.get('latitude', 0)
            lng = geo_point.get('longitude', 0)
            
            # Create point geometry
            point = ee.Geometry.Point([lng, lat])
            
            # Create buffer around the point
            roi = point.buffer(buffer_meters)
            
            self.logger.info(f"Created ROI: {lat}, {lng} with {buffer_meters}m buffer")
            return roi
            
        except Exception as e:
            self.logger.error(f"Error creating ROI: {str(e)}")
            raise
    
    def get_time_periods(self, trigger_date: datetime) -> Tuple[ee.Date, ee.Date, ee.Date, ee.Date]:
        """Define before and after time periods for analysis"""
        try:
            # Before period: 6-9 months before trigger date
            before_start = trigger_date - timedelta(days=270)  # 9 months
            before_end = trigger_date - timedelta(days=180)    # 6 months
            
            # After period: Most recent 1-2 months
            after_start = trigger_date - timedelta(days=60)    # 2 months
            after_end = trigger_date + timedelta(days=1)       # Current date
            
            # Convert to Earth Engine dates
            before_start_ee = ee.Date(before_start.isoformat())
            before_end_ee = ee.Date(before_end.isoformat())
            after_start_ee = ee.Date(after_start.isoformat())
            after_end_ee = ee.Date(after_end.isoformat())
            
            self.logger.info(f"Time periods - Before: {before_start} to {before_end}, After: {after_start} to {after_end}")
            
            return before_start_ee, before_end_ee, after_start_ee, after_end_ee
            
        except Exception as e:
            self.logger.error(f"Error defining time periods: {str(e)}")
            raise
    
    def get_sentinel2_image(self, roi: ee.Geometry, start_date: ee.Date, end_date: ee.Date) -> Optional[ee.Image]:
        """Get the best Sentinel-2 image for the given time period and ROI"""
        try:
            # Query Sentinel-2 collection
            collection = (ee.ImageCollection('COPERNICUS/S2_SR')
                         .filterBounds(roi)
                         .filterDate(start_date, end_date)
                         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))  # Less than 20% cloud cover
            
            # Get image count
            count = collection.size()
            count_value = count.getInfo()
            
            if count_value == 0:
                self.logger.warning(f"No suitable Sentinel-2 images found for period {start_date} to {end_date}")
                return None
            
            # Select image with least cloud cover
            best_image = collection.sort('CLOUDY_PIXEL_PERCENTAGE').first()
            
            # Clip to ROI
            clipped_image = best_image.clip(roi)
            
            self.logger.info(f"Selected Sentinel-2 image with {best_image.get('CLOUDY_PIXEL_PERCENTAGE').getInfo()}% cloud cover")
            return clipped_image
            
        except Exception as e:
            self.logger.error(f"Error getting Sentinel-2 image: {str(e)}")
            return None
    
    def calculate_ndbi(self, image: ee.Image) -> ee.Image:
        """Calculate Normalized Difference Built-up Index (NDBI)"""
        try:
            # For Sentinel-2: NDBI = (B11 - B8) / (B11 + B8)
            # B11 = SWIR1 (Short Wave Infrared 1)
            # B8 = NIR (Near Infrared)
            nir = image.select('B8')
            swir1 = image.select('B11')
            
            # Calculate NDBI
            ndbi = swir1.subtract(nir).divide(swir1.add(nir))
            
            return ndbi
            
        except Exception as e:
            self.logger.error(f"Error calculating NDBI: {str(e)}")
            raise
    
    def calculate_mean_ndbi(self, ndbi_image: ee.Image, roi: ee.Geometry) -> float:
        """Calculate mean NDBI value within the ROI"""
        try:
            # Calculate mean NDBI within the ROI
            mean_ndbi = ndbi_image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=roi,
                scale=10,  # 10m resolution for Sentinel-2
                maxPixels=1e9
            )
            
            # Get the result
            result = mean_ndbi.getInfo()
            mean_value = result.get('B8', 0)  # NDBI is stored in B8 band
            
            self.logger.info(f"Mean NDBI value: {mean_value}")
            return mean_value
            
        except Exception as e:
            self.logger.error(f"Error calculating mean NDBI: {str(e)}")
            return 0.0
    
    def analyze_project_progress(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main analysis function for project progress verification"""
        try:
            self.logger.info(f"Starting satellite analysis for project: {project_data.get('projectName', 'Unknown')}")
            
            # Extract project information
            geo_point = project_data.get('geoPoint')
            project_name = project_data.get('projectName', 'Unknown Project')
            project_status = project_data.get('status', 'Unknown')
            start_date = project_data.get('startDate')
            
            if not geo_point:
                self.logger.error("No geoPoint found in project data")
                return {'error': 'No geoPoint found'}
            
            # Create ROI
            roi = self.get_project_roi(geo_point)
            
            # Define time periods
            trigger_date = datetime.now()
            if start_date:
                # Convert Firestore timestamp to datetime
                if hasattr(start_date, 'to_pydatetime'):
                    trigger_date = start_date.to_pydatetime()
                elif isinstance(start_date, str):
                    trigger_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            
            before_start, before_end, after_start, after_end = self.get_time_periods(trigger_date)
            
            # Get satellite images
            before_image = self.get_sentinel2_image(roi, before_start, before_end)
            after_image = self.get_sentinel2_image(roi, after_start, after_end)
            
            if not before_image or not after_image:
                self.logger.warning("Could not obtain suitable satellite images for analysis")
                return {'error': 'No suitable satellite images available'}
            
            # Calculate NDBI for both images
            before_ndbi = self.calculate_ndbi(before_image)
            after_ndbi = self.calculate_ndbi(after_image)
            
            # Calculate mean NDBI values
            before_mean = self.calculate_mean_ndbi(before_ndbi, roi)
            after_mean = self.calculate_mean_ndbi(after_ndbi, roi)
            
            # Calculate percentage change
            if before_mean != 0:
                ndbi_change_percent = ((after_mean - before_mean) / abs(before_mean)) * 100
            else:
                ndbi_change_percent = 0
            
            # Analyze the change
            analysis_result = self.analyze_ndbi_change(
                ndbi_change_percent, 
                project_status, 
                trigger_date, 
                start_date
            )
            
            # Create analysis summary
            analysis_summary = {
                'projectName': project_name,
                'projectStatus': project_status,
                'beforeMeanNDBI': before_mean,
                'afterMeanNDBI': after_mean,
                'ndbiChangePercent': ndbi_change_percent,
                'analysisDate': datetime.now().isoformat(),
                'timePeriods': {
                    'before': f"{before_start.getInfo()['value']} to {before_end.getInfo()['value']}",
                    'after': f"{after_start.getInfo()['value']} to {after_end.getInfo()['value']}"
                },
                'roiBuffer': 500,  # meters
                'analysisResult': analysis_result
            }
            
            self.logger.info(f"Analysis completed. NDBI change: {ndbi_change_percent:.2f}%")
            return analysis_summary
            
        except Exception as e:
            self.logger.error(f"Error in project progress analysis: {str(e)}")
            return {'error': str(e)}
    
    def analyze_ndbi_change(self, ndbi_change_percent: float, project_status: str, 
                           trigger_date: datetime, start_date: Optional[datetime]) -> Dict[str, Any]:
        """Analyze NDBI change and determine if there's a mismatch"""
        try:
            # Calculate project duration in months
            project_duration_months = 0
            if start_date:
                if hasattr(start_date, 'to_pydatetime'):
                    start_dt = start_date.to_pydatetime()
                elif isinstance(start_date, str):
                    start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                else:
                    start_dt = start_date
                
                duration = trigger_date - start_dt
                project_duration_months = duration.days / 30.44  # Average days per month
            
            # Define expected NDBI changes based on project status and duration
            expected_changes = {
                'Pending': {'min_change': 0, 'max_change': 5},
                'In Progress': {'min_change': 5, 'max_change': 50},
                'Completed': {'min_change': 10, 'max_change': 100},
                'Cancelled': {'min_change': 0, 'max_change': 10}
            }
            
            expected = expected_changes.get(project_status, {'min_change': 0, 'max_change': 100})
            
            # Determine if there's a mismatch
            is_mismatch = False
            severity = 'low'
            mismatch_reason = ''
            
            if project_status in ['In Progress', 'Completed']:
                if ndbi_change_percent < expected['min_change']:
                    is_mismatch = True
                    if project_duration_months > 6:
                        severity = 'high'
                        mismatch_reason = f"Project has been {project_status.lower()} for {project_duration_months:.1f} months but shows minimal physical change ({ndbi_change_percent:.1f}%)"
                    else:
                        severity = 'medium'
                        mismatch_reason = f"Project status is {project_status} but shows low physical change ({ndbi_change_percent:.1f}%)"
                elif ndbi_change_percent > expected['max_change']:
                    severity = 'medium'
                    mismatch_reason = f"Unexpectedly high physical change detected ({ndbi_change_percent:.1f}%) for {project_status} project"
            
            return {
                'isMismatch': is_mismatch,
                'severity': severity,
                'mismatchReason': mismatch_reason,
                'expectedChange': expected,
                'actualChange': ndbi_change_percent,
                'projectDurationMonths': project_duration_months,
                'confidence': self.calculate_confidence(ndbi_change_percent, project_duration_months)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing NDBI change: {str(e)}")
            return {'isMismatch': False, 'severity': 'low', 'error': str(e)}
    
    def calculate_confidence(self, ndbi_change: float, duration_months: float) -> str:
        """Calculate confidence level for the analysis"""
        try:
            # Higher confidence for longer projects with significant changes
            if duration_months > 6 and abs(ndbi_change) > 10:
                return 'high'
            elif duration_months > 3 and abs(ndbi_change) > 5:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {str(e)}")
            return 'low'
    
    def create_red_flag(self, project_id: str, analysis_result: Dict[str, Any]) -> bool:
        """Create a red flag if significant mismatch is detected"""
        try:
            if not analysis_result.get('analysisResult', {}).get('isMismatch', False):
                return False
            
            analysis = analysis_result['analysisResult']
            
            # Create red flag document
            red_flag = {
                'flagType': 'Satellite Verification Mismatch',
                'description': f"Low change in physical structures detected from satellite imagery despite the project being {analysis_result['projectStatus'].lower()} for {analysis.get('projectDurationMonths', 0):.1f} months. Verified change: {analysis_result['ndbiChangePercent']:.1f}%.",
                'linkedProjectIds': [project_id],
                'linkedDonationIds': [],
                'severity': analysis.get('severity', 'medium'),
                'detectedAt': datetime.now(),
                'source': 'satellite_inspector',
                'analysisDetails': {
                    'beforeMeanNDBI': analysis_result.get('beforeMeanNDBI', 0),
                    'afterMeanNDBI': analysis_result.get('afterMeanNDBI', 0),
                    'ndbiChangePercent': analysis_result.get('ndbiChangePercent', 0),
                    'confidence': analysis.get('confidence', 'low')
                }
            }
            
            # Save to Firestore
            self.db.collection('aiRedFlags').add(red_flag)
            
            self.logger.info(f"Created red flag for project {project_id}: {red_flag['description']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating red flag: {str(e)}")
            return False
    
    def save_analysis_result(self, project_id: str, analysis_result: Dict[str, Any]) -> bool:
        """Save analysis result to the project document"""
        try:
            # Update project document with satellite analysis
            project_ref = self.db.collection('projects').document(project_id)
            project_ref.update({
                'satelliteAnalysis': analysis_result,
                'lastSatelliteAnalysis': datetime.now()
            })
            
            self.logger.info(f"Saved satellite analysis for project {project_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving analysis result: {str(e)}")
            return False
    
    def process_project(self, project_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function for a single project"""
        try:
            self.logger.info(f"Processing project: {project_id}")
            
            # Perform satellite analysis
            analysis_result = self.analyze_project_progress(project_data)
            
            if 'error' in analysis_result:
                return analysis_result
            
            # Save analysis result
            self.save_analysis_result(project_id, analysis_result)
            
            # Create red flag if necessary
            self.create_red_flag(project_id, analysis_result)
            
            return {
                'success': True,
                'projectId': project_id,
                'analysisResult': analysis_result
            }
            
        except Exception as e:
            self.logger.error(f"Error processing project {project_id}: {str(e)}")
            return {'error': str(e)}

def main():
    """Main function for testing or Cloud Function execution"""
    inspector = SatelliteInspector()
    
    # Check if running from Cloud Function (with PROJECT_DATA env var)
    project_data_json = os.environ.get('PROJECT_DATA')
    if project_data_json:
        try:
            project_data = json.loads(project_data_json)
            project_id = project_data.get('projectId')
            
            if not project_id:
                print("Error: No projectId found in PROJECT_DATA")
                sys.exit(1)
            
            # Process the project
            result = inspector.process_project(project_id, project_data)
            print(json.dumps(result, indent=2, default=str))
            
        except Exception as e:
            print(f"Error processing project from Cloud Function: {str(e)}")
            sys.exit(1)
    else:
        # Test with sample project data
        sample_project = {
            'projectName': 'Test Road Construction',
            'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946},
            'status': 'In Progress',
            'startDate': datetime.now() - timedelta(days=180)
        }
        
        result = inspector.process_project('test-project-id', sample_project)
        print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
