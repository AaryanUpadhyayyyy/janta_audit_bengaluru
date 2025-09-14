import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_health_engine.fusion_engine import FusionEngine
from hybrid_health_engine.base import DigitalProgress, PhysicalProgress

def main():
    # Load environment variables
    load_dotenv()

    print("=== Hybrid Project Health Engine ===")
    
    # Initialize fusion engine
    config = {
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
    
    engine = FusionEngine(config)
    if not engine.initialize():
        print("Error: Failed to initialize fusion engine")
        return 1

    # Sample project data
    digital_data = DigitalProgress(
        total_story_points=100,
        completed_points=60,
        sprint_velocity=20,
        pr_merge_rate=0.8,
        commit_frequency=5,
        last_updated=datetime.now()
    )

    physical_data = PhysicalProgress(
        phase="framing",
        completeness=0.5,
        confidence=0.8,
        last_updated=datetime.now(),
        raw_metrics={"detected_objects": 15, "phase_confidence": 0.85}
    )

    target_date = datetime.now() + timedelta(days=30)
    budget_data = {
        "budget": 100000,
        "actual_cost": 45000
    }

    try:
        # Generate metrics
        metrics = engine.fuse_progress_data(
            digital_data,
            physical_data,
            target_date,
            budget_data
        )

        # Display results
        print("\nProject Health Metrics:")
        print("-----------------------")
        print(f"True Progress: {metrics.true_progress_percentage:.1f}%")
        print(f"Predicted Completion: {metrics.predicted_ecd.strftime('%Y-%m-%d')}")
        print(f"Status: {metrics.variance_alert}")
        print(f"Confidence Score: {metrics.confidence_score:.2f}")
        print(f"Cost Performance Index: {metrics.cost_performance_index:.2f}")

        # Show health metrics
        health = engine.get_health_metrics()
        print("\nSystem Health:")
        print("--------------")
        for key, value in health.items():
            print(f"{key}: {value}")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())