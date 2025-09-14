#!/usr/bin/env python3
"""
Standalone script to run satellite analysis for a specific project
This script is called by the Firebase Cloud Function
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from satellite_inspector import SatelliteInspector

def main():
    """Main function to run satellite analysis"""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Get project data from environment variable
        project_data_json = os.environ.get('PROJECT_DATA')
        if not project_data_json:
            logger.error("No PROJECT_DATA environment variable found")
            sys.exit(1)
        
        project_data = json.loads(project_data_json)
        project_id = project_data.get('projectId')
        
        if not project_id:
            logger.error("No projectId found in PROJECT_DATA")
            sys.exit(1)
        
        logger.info(f"Starting satellite analysis for project: {project_id}")
        
        # Initialize satellite inspector
        inspector = SatelliteInspector()
        
        # Process the project
        result = inspector.process_project(project_id, project_data)
        
        if result.get('success'):
            logger.info(f"Satellite analysis completed successfully for project {project_id}")
            print(json.dumps(result, indent=2, default=str))
        else:
            logger.error(f"Satellite analysis failed for project {project_id}: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error in satellite analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
