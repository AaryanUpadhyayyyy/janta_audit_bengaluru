import asyncio
import logging
from pathlib import Path
from typing import Dict, Optional

from config import config
from cv_engine import CVEngine
from data_ingestors import JiraIngestor, GitHubIngestor, ImageIngestor
from digital_engine import DigitalVelocityEngine
from fusion_engine import FusionEngine

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if config.system_config['debug'] else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HybridHealthEngine:
    """Main entry point for the Hybrid Project Health Engine"""
    
    def __init__(self):
        self.cv_engine = CVEngine(config.cv_config)
        self.digital_engine = DigitalVelocityEngine()
        self.fusion_engine = FusionEngine(config.system_config)
        
        self.jira_ingestor = JiraIngestor(config.jira_config)
        self.github_ingestor = GitHubIngestor(config.github_config)
        self.image_ingestor = ImageIngestor({
            'image_dir': str(config.data_dir / 'images'),
            'drone_upload_dir': str(config.data_dir / 'drone')
        })
        
    async def initialize(self) -> bool:
        """Initialize all components"""
        try:
            # Initialize engines
            cv_init = self.cv_engine.initialize()
            digital_init = self.digital_engine.initialize()
            fusion_init = self.fusion_engine.initialize()
            
            if not all([cv_init, digital_init, fusion_init]):
                logger.error("Failed to initialize one or more engines")
                return False
            
            # Test data ingestion
            jira_data = await self.jira_ingestor.fetch_data()
            github_data = await self.github_ingestor.fetch_data()
            image_data = await self.image_ingestor.fetch_data()
            
            if not all([
                await self.jira_ingestor.validate_data(jira_data),
                await self.github_ingestor.validate_data(github_data),
                await self.image_ingestor.validate_data(image_data)
            ]):
                logger.error("Data validation failed for one or more sources")
                return False
                
            logger.info("Successfully initialized Hybrid Health Engine")
            return True
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            return False
            
    async def analyze_project_health(self) -> Dict:
        """Run a complete project health analysis"""
        try:
            # Fetch all required data
            jira_data = await self.jira_ingestor.fetch_data()
            github_data = await self.github_ingestor.fetch_data()
            image_data = await self.image_ingestor.fetch_data()
            
            # Process digital progress
            digital_metrics = await self.jira_ingestor.preprocess_data(jira_data)
            github_metrics = await self.github_ingestor.preprocess_data(github_data)
            
            digital_progress = {
                **digital_metrics,
                **github_metrics
            }
            
            # Process physical progress
            image_data = await self.image_ingestor.preprocess_data(image_data)
            physical_progress = self.cv_engine.predict(image_data)
            
            # Fuse progress data
            fused_metrics = self.fusion_engine.fuse_progress_data(
                digital_progress,
                physical_progress,
                target_date=config.project_target_date,
                budget_data=config.budget_data
            )
            
            return {
                'digital_progress': digital_progress,
                'physical_progress': physical_progress,
                'fused_metrics': fused_metrics,
                'health_metrics': {
                    'cv_engine': self.cv_engine.get_health_metrics(),
                    'digital_engine': self.digital_engine.get_health_metrics(),
                    'fusion_engine': self.fusion_engine.get_health_metrics()
                }
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return None

async def main():
    """Main entry point"""
    engine = HybridHealthEngine()
    
    logger.info("Initializing Hybrid Health Engine...")
    if await engine.initialize():
        logger.info("Running project health analysis...")
        results = await engine.analyze_project_health()
        
        if results:
            logger.info("Analysis completed successfully!")
            logger.debug(f"Results: {results}")
        else:
            logger.error("Analysis failed!")
    else:
        logger.error("Initialization failed!")

if __name__ == "__main__":
    asyncio.run(main())