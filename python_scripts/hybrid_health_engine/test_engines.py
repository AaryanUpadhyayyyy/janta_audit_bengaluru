import logging
from datetime import datetime, timedelta
import numpy as np
import torch
from pathlib import Path

from config import config
from cv_engine import CVEngine
from digital_engine import DigitalVelocityEngine
from fusion_engine import FusionEngine
from base import DigitalProgress, PhysicalProgress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_cv_engine():
    """Test Computer Vision Engine"""
    logger.info("Testing CV Engine...")
    try:
        # Create a dummy model file
        model_path = Path(config.cv_config['model_path'])
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a simple dummy PyTorch model
        class DummyModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.conv = torch.nn.Conv2d(3, 5, 3)
                self.completeness_head = torch.nn.Linear(100, 1)
                
            def forward(self, x):
                return self.conv(x)
        
        dummy_model = DummyModel()
        torch.save(dummy_model, model_path)
        
        # Initialize CV engine
        engine = CVEngine(config.cv_config)
        if not engine.initialize():
            logger.error("CV Engine initialization failed")
            return False
            
        # Test prediction with dummy data
        dummy_image = np.random.rand(512, 512, 3) * 255
        result = engine.predict(dummy_image)
        
        if result is None:
            logger.error("CV Engine prediction failed")
            return False
            
        logger.info("CV Engine test passed!")
        return True
        
    except Exception as e:
        logger.error(f"CV Engine test failed: {e}")
        return False

def test_digital_engine():
    """Test Digital Velocity Engine"""
    logger.info("Testing Digital Velocity Engine...")
    try:
        engine = DigitalVelocityEngine()
        if not engine.initialize():
            logger.error("Digital Engine initialization failed")
            return False
            
        # Test with sample data
        digital_progress = DigitalProgress(
            total_story_points=100,
            completed_points=45,
            sprint_velocity=10.5,
            commit_frequency=5.2,
            pr_merge_rate=0.85,
            last_updated=datetime.now()
        )
        
        prediction = engine.predict_completion(
            digital_progress,
            target_points=100,
            confidence_level=0.8
        )
        
        if prediction['predicted_date'] is None:
            logger.error("Digital Engine prediction failed")
            return False
            
        logger.info("Digital Engine test passed!")
        return True
        
    except Exception as e:
        logger.error(f"Digital Engine test failed: {e}")
        return False

def test_fusion_engine():
    """Test Fusion Engine"""
    logger.info("Testing Fusion Engine...")
    try:
        engine = FusionEngine(config.system_config)
        if not engine.initialize():
            logger.error("Fusion Engine initialization failed")
            return False
            
        # Test with sample data
        digital_progress = DigitalProgress(
            total_story_points=100,
            completed_points=45,
            sprint_velocity=10.5,
            commit_frequency=5.2,
            pr_merge_rate=0.85,
            last_updated=datetime.now()
        )
        
        physical_progress = PhysicalProgress(
            phase="framing",
            completeness=0.4,
            confidence=0.85,
            last_updated=datetime.now(),
            raw_metrics={
                "unadjusted_completeness": 0.45,
                "phase_threshold": 0.75
            }
        )
        
        target_date = datetime.now() + timedelta(days=90)
        budget_data = {
            "budget": 1000000,
            "actual_cost": 400000
        }
        
        metrics = engine.fuse_progress_data(
            digital_progress,
            physical_progress,
            target_date,
            budget_data
        )
        
        if metrics is None:
            logger.error("Fusion Engine metrics calculation failed")
            return False
            
        logger.info("Fusion Engine test passed!")
        return True
        
    except Exception as e:
        logger.error(f"Fusion Engine test failed: {e}")
        return False

def main():
    """Run all engine tests"""
    results = {
        "CV Engine": test_cv_engine(),
        "Digital Engine": test_digital_engine(),
        "Fusion Engine": test_fusion_engine()
    }
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("All engine tests passed!")
    else:
        logger.error("Some engine tests failed!")
        failed_tests = [
            name for name, passed in results.items()
            if not passed
        ]
        logger.error(f"Failed tests: {', '.join(failed_tests)}")
        
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())