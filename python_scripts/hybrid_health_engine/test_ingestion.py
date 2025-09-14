import asyncio
import logging
from pathlib import Path

from config import config
from data_ingestors import JiraIngestor, GitHubIngestor, ImageIngestor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_jira_ingestion():
    """Test Jira data ingestion"""
    logger.info("Testing Jira ingestion...")
    try:
        ingestor = JiraIngestor(config.jira_config)
        data = await ingestor.fetch_data()
        
        if await ingestor.validate_data(data):
            processed_data = await ingestor.preprocess_data(data)
            logger.info("Jira ingestion successful!")
            logger.debug(f"Processed data: {processed_data}")
            return True
    except Exception as e:
        logger.error(f"Jira ingestion failed: {e}")
    return False

async def test_github_ingestion():
    """Test GitHub data ingestion"""
    logger.info("Testing GitHub ingestion...")
    try:
        ingestor = GitHubIngestor(config.github_config)
        data = await ingestor.fetch_data()
        
        if await ingestor.validate_data(data):
            processed_data = await ingestor.preprocess_data(data)
            logger.info("GitHub ingestion successful!")
            logger.debug(f"Processed data: {processed_data}")
            return True
    except Exception as e:
        logger.error(f"GitHub ingestion failed: {e}")
    return False

async def test_image_ingestion():
    """Test image data ingestion"""
    logger.info("Testing image ingestion...")
    try:
        # Create some test images
        image_dir = Path(config.data_dir) / 'images'
        drone_dir = Path(config.data_dir) / 'drone'
        
        # Create test files
        test_files = [
            image_dir / 'test1.jpg',
            image_dir / 'test2.jpg',
            drone_dir / 'drone1.jpg',
            drone_dir / 'video1.mp4'
        ]
        
        for file_path in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if not file_path.exists():
                file_path.touch()
        
        ingestor = ImageIngestor({
            'image_dir': str(image_dir),
            'drone_upload_dir': str(drone_dir)
        })
        
        data = await ingestor.fetch_data()
        
        if await ingestor.validate_data(data):
            processed_data = await ingestor.preprocess_data(data)
            logger.info("Image ingestion successful!")
            logger.debug(f"Processed data: {processed_data}")
            
            # Cleanup test files
            for file_path in test_files:
                file_path.unlink()
            
            return True
    except Exception as e:
        logger.error(f"Image ingestion failed: {e}")
    return False

async def main():
    """Run all ingestion tests"""
    results = await asyncio.gather(
        test_jira_ingestion(),
        test_github_ingestion(),
        test_image_ingestion()
    )
    
    all_passed = all(results)
    
    if all_passed:
        logger.info("All ingestion tests passed!")
    else:
        logger.error("Some ingestion tests failed!")
        failed_tests = [
            test_name for test_name, passed in zip(
                ['Jira', 'GitHub', 'Image'],
                results
            ) if not passed
        ]
        logger.error(f"Failed tests: {', '.join(failed_tests)}")

if __name__ == "__main__":
    asyncio.run(main())