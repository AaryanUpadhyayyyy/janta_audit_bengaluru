import unittest
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_health_engine.fusion_engine import FusionEngine
from hybrid_health_engine.base import DigitalProgress, PhysicalProgress

class TestFusionEngine(unittest.TestCase):
    def setUp(self):
        self.config = {
            "phase_weights": {
                "foundation": 0.2,
                "framing": 0.3,
                "exterior": 0.2,
                "interior": 0.2,
                "finishing": 0.1
            },
            "variance_thresholds": {
                "yellow": 0.15,
                "red": 0.25
            }
        }
        self.engine = FusionEngine(self.config)
        self.engine.initialize()

    def test_basic_fusion(self):
        # Test data
        digital_data = DigitalProgress(
            total_story_points=100,
            completed_points=60,
            sprint_velocity=20,
            pr_merge_rate=0.8,
            commit_frequency=5
        )

        physical_data = PhysicalProgress(
            phase="framing",
            completeness=0.5,
            confidence=0.8
        )

        target_date = datetime.now() + timedelta(days=30)
        budget_data = {
            "budget": 100000,
            "actual_cost": 45000
        }

        # Get fused metrics
        metrics = self.engine.fuse_progress_data(
            digital_data,
            physical_data,
            target_date,
            budget_data
        )

        # Assertions
        self.assertIsNotNone(metrics)
        self.assertTrue(0 <= metrics.true_progress_percentage <= 100)
        self.assertTrue(0 <= metrics.confidence_score <= 1)
        self.assertTrue(metrics.cost_performance_index > 0)

    def test_physical_bottleneck(self):
        """Test that physical progress acts as a bottleneck"""
        digital_data = DigitalProgress(
            total_story_points=100,
            completed_points=80,  # 80% complete
            sprint_velocity=20,
            pr_merge_rate=0.9,
            commit_frequency=5
        )

        physical_data = PhysicalProgress(
            phase="framing",
            completeness=0.4,  # 40% complete
            confidence=0.9
        )

        target_date = datetime.now() + timedelta(days=30)
        budget_data = {
            "budget": 100000,
            "actual_cost": 45000
        }

        metrics = self.engine.fuse_progress_data(
            digital_data,
            physical_data,
            target_date,
            budget_data
        )

        # True progress should be limited by physical progress
        self.assertLessEqual(metrics.true_progress_percentage, 40.0)

    def test_variance_alerts(self):
        """Test variance alert thresholds"""
        digital_data = DigitalProgress(
            total_story_points=100,
            completed_points=80,
            sprint_velocity=20,
            pr_merge_rate=0.9,
            commit_frequency=5
        )

        physical_data = PhysicalProgress(
            phase="framing",
            completeness=0.4,
            confidence=0.9
        )

        target_date = datetime.now() + timedelta(days=30)
        budget_data = {
            "budget": 100000,
            "actual_cost": 45000
        }

        metrics = self.engine.fuse_progress_data(
            digital_data,
            physical_data,
            target_date,
            budget_data
        )

        # With this large variance (80% vs 40%), should get RED alert
        self.assertEqual(metrics.variance_alert, "RED")

if __name__ == '__main__':
    unittest.main()