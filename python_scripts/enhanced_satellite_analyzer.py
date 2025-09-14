#!/usr/bin/env python3
"""
Enhanced Satellite Analyzer for Janata Audit Bengaluru
Uses free APIs and AI to analyze project locations with time period detection
"""

import os
import sys
import logging
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, List
import cv2
from PIL import Image
import io
import base64
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import ee
import firebase_admin
from firebase_admin import firestore

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class FreeSatelliteAnalyzer:
    """Enhanced satellite analyzer using free APIs and AI"""
    
    def __init__(self):
        self.setup_logging()
        self.initialize_services()
        self.setup_free_apis()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_satellite_analyzer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_services(self):
        """Initialize Firebase and other services"""
        try:
            # Initialize Firebase Admin (if not already initialized)
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            
            self.db = firestore.client()
            self.logger.info("Services initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing services: {str(e)}")
            raise
    
    def setup_free_apis(self):
        """Setup free API configurations"""
        self.api_configs = {
            'overpass': 'https://overpass-api.de/api/interpreter',
            'nominatim': 'https://nominatim.openstreetmap.org',
            'opentopomap': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            'cartodb': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            'esri_satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            'usgs_earthdata': 'https://e4ftl01.cr.usgs.gov',
            'sentinel_hub': 'https://services.sentinel-hub.com/api/v1'
        }
    
    def get_location_info(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get location information using free APIs"""
        try:
            # Use Nominatim for reverse geocoding
            url = f"{self.api_configs['nominatim']}/reverse"
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'addressdetails': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            location_info = {
                'address': data.get('display_name', ''),
                'city': data.get('address', {}).get('city', ''),
                'state': data.get('address', {}).get('state', ''),
                'country': data.get('address', {}).get('country', ''),
                'postcode': data.get('address', {}).get('postcode', ''),
                'latitude': latitude,
                'longitude': longitude
            }
            
            self.logger.info(f"Location info retrieved: {location_info['city']}, {location_info['state']}")
            return location_info
            
        except Exception as e:
            self.logger.error(f"Error getting location info: {str(e)}")
            return {'error': str(e)}
    
    def get_satellite_image_url(self, lat: float, lng: float, zoom: int = 16, 
                               size: str = "512x512", source: str = "esri") -> str:
        """Get satellite image URL from free sources"""
        try:
            if source == "esri":
                # Use Esri World Imagery (free)
                return f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox={lng-0.001},{lat-0.001},{lng+0.001},{lat+0.001}&bboxSR=4326&imageSR=4326&size={size}&f=image"
            elif source == "bing":
                # Note: Bing requires API key, but we can use static tiles
                return f"https://ecn.t3.tiles.virtualearth.net/tiles/a{self._get_quad_key(lat, lng, zoom)}.jpeg?g=1"
            else:
                # Default to Esri
                return f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox={lng-0.001},{lat-0.001},{lng+0.001},{lat+0.001}&bboxSR=4326&imageSR=4326&size={size}&f=image"
                
        except Exception as e:
            self.logger.error(f"Error generating satellite image URL: {str(e)}")
            return ""
    
    def _get_quad_key(self, lat: float, lng: float, zoom: int) -> str:
        """Generate quad key for Bing Maps (simplified)"""
        # This is a simplified implementation
        # In production, you'd need proper quad key generation
        return f"{zoom}_{int(lat*1000)}_{int(lng*1000)}"
    
    def download_satellite_image(self, lat: float, lng: float, zoom: int = 16) -> Optional[np.ndarray]:
        """Download satellite image from free sources"""
        try:
            url = self.get_satellite_image_url(lat, lng, zoom)
            if not url:
                return None
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Convert to OpenCV format
            image = Image.open(io.BytesIO(response.content))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            self.logger.info(f"Downloaded satellite image: {image_cv.shape}")
            return image_cv
            
        except Exception as e:
            self.logger.error(f"Error downloading satellite image: {str(e)}")
            return None
    
    def analyze_image_features(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze satellite image using computer vision"""
        try:
            if image is None:
                return {'error': 'No image provided'}
            
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate various features
            features = {
                'mean_brightness': np.mean(gray),
                'std_brightness': np.std(gray),
                'edge_density': self._calculate_edge_density(gray),
                'texture_complexity': self._calculate_texture_complexity(gray),
                'color_diversity': self._calculate_color_diversity(image),
                'built_up_index': self._calculate_built_up_index(image),
                'vegetation_index': self._calculate_vegetation_index(image),
                'water_index': self._calculate_water_index(image)
            }
            
            # Detect structures
            structures = self._detect_structures(image)
            features['structures'] = structures
            
            # Detect changes over time (if historical data available)
            features['change_indicators'] = self._detect_change_indicators(image)
            
            self.logger.info(f"Image features calculated: {len(features)} features")
            return features
            
        except Exception as e:
            self.logger.error(f"Error analyzing image features: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_edge_density(self, gray_image: np.ndarray) -> float:
        """Calculate edge density using Canny edge detection"""
        try:
            edges = cv2.Canny(gray_image, 50, 150)
            edge_pixels = np.sum(edges > 0)
            total_pixels = edges.shape[0] * edges.shape[1]
            return edge_pixels / total_pixels
        except:
            return 0.0
    
    def _calculate_texture_complexity(self, gray_image: np.ndarray) -> float:
        """Calculate texture complexity using local binary patterns"""
        try:
            # Simplified texture analysis
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
            return np.mean(gradient_magnitude)
        except:
            return 0.0
    
    def _calculate_color_diversity(self, image: np.ndarray) -> float:
        """Calculate color diversity in the image"""
        try:
            # Convert to HSV and calculate color histogram
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
            # Calculate entropy of histogram
            hist = hist.flatten()
            hist = hist / hist.sum()
            hist = hist[hist > 0]  # Remove zeros
            entropy = -np.sum(hist * np.log2(hist))
            return entropy
        except:
            return 0.0
    
    def _calculate_built_up_index(self, image: np.ndarray) -> float:
        """Calculate built-up area index"""
        try:
            # Simplified NDBI calculation
            b, g, r = cv2.split(image)
            # Approximate NIR as red channel, SWIR as blue channel
            ndbi = (b.astype(float) - r.astype(float)) / (b.astype(float) + r.astype(float) + 1e-10)
            return np.mean(ndbi)
        except:
            return 0.0
    
    def _calculate_vegetation_index(self, image: np.ndarray) -> float:
        """Calculate vegetation index"""
        try:
            b, g, r = cv2.split(image)
            # Simplified NDVI calculation
            ndvi = (g.astype(float) - r.astype(float)) / (g.astype(float) + r.astype(float) + 1e-10)
            return np.mean(ndvi)
        except:
            return 0.0
    
    def _calculate_water_index(self, image: np.ndarray) -> float:
        """Calculate water index"""
        try:
            b, g, r = cv2.split(image)
            # Simplified water index
            water_idx = (b.astype(float) - r.astype(float)) / (b.astype(float) + r.astype(float) + 1e-10)
            return np.mean(water_idx)
        except:
            return 0.0
    
    def _detect_structures(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect structures in the image"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect lines (roads, buildings)
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
            
            # Detect circles (round structures)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=50)
            
            # Detect rectangles (buildings)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            rectangles = []
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 4:
                    rectangles.append(approx)
            
            return {
                'line_count': len(lines) if lines is not None else 0,
                'circle_count': len(circles[0]) if circles is not None else 0,
                'rectangle_count': len(rectangles),
                'total_structures': (len(lines) if lines is not None else 0) + 
                                 (len(circles[0]) if circles is not None else 0) + 
                                 len(rectangles)
            }
        except Exception as e:
            self.logger.error(f"Error detecting structures: {str(e)}")
            return {'error': str(e)}
    
    def _detect_change_indicators(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect indicators of recent changes"""
        try:
            # This would typically compare with historical images
            # For now, we'll analyze current image for change indicators
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect areas with high contrast (potential construction)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            high_contrast = np.sum(np.abs(laplacian) > np.percentile(np.abs(laplacian), 90))
            
            # Detect straight lines (potential new construction)
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30, minLineLength=20, maxLineGap=5)
            
            return {
                'high_contrast_areas': high_contrast,
                'recent_lines': len(lines) if lines is not None else 0,
                'change_probability': min(1.0, (high_contrast + (len(lines) if lines is not None else 0)) / 1000)
            }
        except Exception as e:
            self.logger.error(f"Error detecting change indicators: {str(e)}")
            return {'error': str(e)}
    
    def analyze_project_location(self, latitude: float, longitude: float, 
                               project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main analysis function for project location"""
        try:
            self.logger.info(f"Starting analysis for location: {latitude}, {longitude}")
            
            # Get location information
            location_info = self.get_location_info(latitude, longitude)
            
            # Download satellite image
            satellite_image = self.download_satellite_image(latitude, longitude)
            
            if satellite_image is None:
                return {'error': 'Could not download satellite image'}
            
            # Analyze image features
            image_features = self.analyze_image_features(satellite_image)
            
            # Determine project status based on analysis
            project_status = self._determine_project_status(image_features, project_data)
            
            # Calculate time period analysis
            time_analysis = self._analyze_time_periods(image_features, project_data)
            
            # Generate comprehensive report
            analysis_report = {
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'address': location_info.get('address', ''),
                    'city': location_info.get('city', ''),
                    'state': location_info.get('state', '')
                },
                'image_analysis': image_features,
                'project_status': project_status,
                'time_analysis': time_analysis,
                'analysis_timestamp': datetime.now().isoformat(),
                'confidence_score': self._calculate_confidence_score(image_features, project_data),
                'recommendations': self._generate_recommendations(image_features, project_status)
            }
            
            self.logger.info(f"Analysis completed for location: {latitude}, {longitude}")
            return analysis_report
            
        except Exception as e:
            self.logger.error(f"Error in project location analysis: {str(e)}")
            return {'error': str(e)}
    
    def _determine_project_status(self, image_features: Dict[str, Any], 
                                project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine project status based on image analysis"""
        try:
            # Get project information
            reported_status = project_data.get('status', 'Unknown')
            start_date = project_data.get('startDate')
            end_date = project_data.get('endDate')
            
            # Calculate project duration
            duration_months = 0
            if start_date:
                if hasattr(start_date, 'to_pydatetime'):
                    start_dt = start_date.to_pydatetime()
                else:
                    start_dt = datetime.fromisoformat(str(start_date).replace('Z', '+00:00'))
                duration_months = (datetime.now() - start_dt).days / 30.44
            
            # Analyze features to determine actual status
            built_up_index = image_features.get('built_up_index', 0)
            structure_count = image_features.get('structures', {}).get('total_structures', 0)
            change_probability = image_features.get('change_indicators', {}).get('change_probability', 0)
            
            # Determine status based on analysis
            if built_up_index > 0.3 and structure_count > 10:
                actual_status = 'Completed'
                confidence = 0.8
            elif change_probability > 0.5 or structure_count > 5:
                actual_status = 'In Progress'
                confidence = 0.7
            elif built_up_index < 0.1 and structure_count < 3:
                actual_status = 'Pending'
                confidence = 0.6
            else:
                actual_status = 'Unknown'
                confidence = 0.4
            
            # Check for mismatches
            status_mismatch = reported_status != actual_status
            
            return {
                'reported_status': reported_status,
                'detected_status': actual_status,
                'confidence': confidence,
                'mismatch': status_mismatch,
                'duration_months': duration_months,
                'indicators': {
                    'built_up_index': built_up_index,
                    'structure_count': structure_count,
                    'change_probability': change_probability
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error determining project status: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_time_periods(self, image_features: Dict[str, Any], 
                            project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze time periods and project progression"""
        try:
            start_date = project_data.get('startDate')
            end_date = project_data.get('endDate')
            current_date = datetime.now()
            
            # Calculate time periods
            if start_date:
                if hasattr(start_date, 'to_pydatetime'):
                    start_dt = start_date.to_pydatetime()
                else:
                    start_dt = datetime.fromisoformat(str(start_date).replace('Z', '+00:00'))
                
                total_duration = (current_date - start_dt).days
                total_months = total_duration / 30.44
            else:
                total_duration = 0
                total_months = 0
            
            # Analyze progression based on image features
            built_up_index = image_features.get('built_up_index', 0)
            structure_count = image_features.get('structures', {}).get('total_structures', 0)
            
            # Estimate completion percentage
            if built_up_index > 0.5:
                completion_percentage = min(100, (built_up_index * 200))
            elif structure_count > 20:
                completion_percentage = min(100, (structure_count * 5))
            else:
                completion_percentage = min(100, (built_up_index * 100 + structure_count * 2))
            
            # Determine if project is on track
            expected_completion = 0
            if total_months > 0:
                # Assume 12 months for typical project
                expected_completion = min(100, (total_months / 12) * 100)
            
            on_track = completion_percentage >= expected_completion * 0.8  # 80% tolerance
            
            return {
                'total_duration_days': total_duration,
                'total_duration_months': total_months,
                'completion_percentage': completion_percentage,
                'expected_completion': expected_completion,
                'on_track': on_track,
                'time_indicators': {
                    'built_up_index': built_up_index,
                    'structure_count': structure_count,
                    'change_probability': image_features.get('change_indicators', {}).get('change_probability', 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing time periods: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_confidence_score(self, image_features: Dict[str, Any], 
                                  project_data: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        try:
            confidence_factors = []
            
            # Image quality factors
            brightness = image_features.get('mean_brightness', 0)
            if 50 < brightness < 200:
                confidence_factors.append(0.2)
            else:
                confidence_factors.append(0.1)
            
            # Feature richness
            edge_density = image_features.get('edge_density', 0)
            if edge_density > 0.1:
                confidence_factors.append(0.2)
            else:
                confidence_factors.append(0.1)
            
            # Structure detection
            structure_count = image_features.get('structures', {}).get('total_structures', 0)
            if structure_count > 5:
                confidence_factors.append(0.3)
            elif structure_count > 0:
                confidence_factors.append(0.2)
            else:
                confidence_factors.append(0.1)
            
            # Change indicators
            change_prob = image_features.get('change_indicators', {}).get('change_probability', 0)
            if change_prob > 0.3:
                confidence_factors.append(0.3)
            else:
                confidence_factors.append(0.1)
            
            total_confidence = sum(confidence_factors)
            return min(1.0, total_confidence)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence score: {str(e)}")
            return 0.5
    
    def _generate_recommendations(self, image_features: Dict[str, Any], 
                                project_status: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        try:
            # Status mismatch recommendations
            if project_status.get('mismatch', False):
                recommendations.append(
                    f"Status mismatch detected: Reported as '{project_status.get('reported_status')}' "
                    f"but analysis suggests '{project_status.get('detected_status')}'. "
                    "Recommend on-site verification."
                )
            
            # Low activity recommendations
            structure_count = image_features.get('structures', {}).get('total_structures', 0)
            if structure_count < 3 and project_status.get('detected_status') == 'In Progress':
                recommendations.append(
                    "Low structural activity detected for 'In Progress' project. "
                    "Recommend checking project status and contractor performance."
                )
            
            # High change probability recommendations
            change_prob = image_features.get('change_indicators', {}).get('change_probability', 0)
            if change_prob > 0.7:
                recommendations.append(
                    "High change probability detected. Recommend monitoring for "
                    "unauthorized construction or project scope changes."
                )
            
            # Time-based recommendations
            duration_months = project_status.get('duration_months', 0)
            if duration_months > 12 and project_status.get('detected_status') != 'Completed':
                recommendations.append(
                    f"Project has been ongoing for {duration_months:.1f} months. "
                    "Recommend reviewing project timeline and budget."
                )
            
            if not recommendations:
                recommendations.append("No specific issues detected. Continue monitoring.")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return ["Error generating recommendations"]
    
    def save_analysis_to_firestore(self, project_id: str, analysis_report: Dict[str, Any]) -> bool:
        """Save analysis report to Firestore"""
        try:
            # Save to projects collection
            project_ref = self.db.collection('projects').document(project_id)
            project_ref.update({
                'enhancedSatelliteAnalysis': analysis_report,
                'lastEnhancedAnalysis': datetime.now()
            })
            
            # Save to analysis collection
            analysis_ref = self.db.collection('satelliteAnalysis').document()
            analysis_doc = {
                'projectId': project_id,
                'analysisReport': analysis_report,
                'createdAt': datetime.now(),
                'analysisType': 'enhanced_satellite'
            }
            analysis_ref.set(analysis_doc)
            
            self.logger.info(f"Analysis saved to Firestore for project {project_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving analysis to Firestore: {str(e)}")
            return False
    
    def process_project_analysis(self, project_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function for project analysis"""
        try:
            self.logger.info(f"Processing enhanced analysis for project: {project_id}")
            
            # Get project location
            geo_point = project_data.get('geoPoint')
            if not geo_point:
                return {'error': 'No geoPoint found in project data'}
            
            latitude = geo_point.get('latitude')
            longitude = geo_point.get('longitude')
            
            if not latitude or not longitude:
                return {'error': 'Invalid coordinates in geoPoint'}
            
            # Perform analysis
            analysis_report = self.analyze_project_location(latitude, longitude, project_data)
            
            if 'error' in analysis_report:
                return analysis_report
            
            # Save to Firestore
            self.save_analysis_to_firestore(project_id, analysis_report)
            
            return {
                'success': True,
                'projectId': project_id,
                'analysisReport': analysis_report
            }
            
        except Exception as e:
            self.logger.error(f"Error processing project analysis {project_id}: {str(e)}")
            return {'error': str(e)}

def main():
    """Main function for testing"""
    analyzer = FreeSatelliteAnalyzer()
    
    # Test with sample project data
    sample_project = {
        'projectName': 'Test Road Construction',
        'geoPoint': {'latitude': 12.9716, 'longitude': 77.5946},
        'status': 'In Progress',
        'startDate': datetime.now() - timedelta(days=180),
        'endDate': datetime.now() + timedelta(days=180)
    }
    
    result = analyzer.process_project_analysis('test-project-id', sample_project)
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
