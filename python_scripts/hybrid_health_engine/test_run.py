from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_health_engine.fusion_engine import FusionEngine
from hybrid_health_engine.base import DigitalProgress, PhysicalProgress

def main():
    print("=== Hybrid Project Health Engine Test ===\n")
    
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
    
    try:
        print("Step 1: Initializing Fusion Engine...")
        engine = FusionEngine(config)
        if not engine.initialize():
            print("❌ Error: Failed to initialize fusion engine")
            return 1
        print("✅ Fusion Engine initialized successfully")

        print("\nStep 2: Preparing Test Data...")
        # Sample project data with timestamps
        current_time = datetime.now()
        digital_data = DigitalProgress(
            total_story_points=100,
            completed_points=60,
            sprint_velocity=20,
            pr_merge_rate=0.8,
            commit_frequency=5,
            last_updated=current_time  # Adding the missing timestamp
        )

        physical_data = PhysicalProgress(
            phase="framing",
            completeness=0.5,
            confidence=0.8,
            last_updated=current_time,  # Adding timestamp
            raw_metrics={
                "detected_objects": 15,
                "phase_confidence": 0.85
            }
        )

        target_date = datetime.now() + timedelta(days=30)
        budget_data = {
            "budget": 100000,
            "actual_cost": 45000
        }
        print("✅ Test data prepared successfully")

        print("\nStep 3: Running Analysis...")
        # Generate metrics
        metrics = engine.fuse_progress_data(
            digital_data,
            physical_data,
            target_date,
            budget_data
        )
        print("✅ Analysis completed successfully")

        print("\nStep 4: Evaluation Results:")
        print("-" * 40)
        print(f"True Progress: {metrics.true_progress_percentage:.1f}%")
        print(f"  └─ This is the verified progress considering both digital and physical constraints")
        
        print(f"\nPredicted Completion: {metrics.predicted_ecd.strftime('%Y-%m-%d')}")
        print(f"  └─ Based on current velocities and physical limitations")
        
        print(f"\nStatus: {metrics.variance_alert}")
        print("  └─ GREEN: On track")
        print("  └─ YELLOW: Minor deviation (>15%)")
        print("  └─ RED: Major deviation (>25%)")
        
        print(f"\nConfidence Score: {metrics.confidence_score:.2f}")
        print("  └─ Reliability of predictions (0-1)")
        
        print(f"\nCost Performance Index: {metrics.cost_performance_index:.2f}")
        print("  └─ >1: Under budget")
        print("  └─ <1: Over budget")

        # Show health metrics
        health = engine.get_health_metrics()
        print("\nStep 5: System Health Metrics:")
        print("-" * 40)
        for key, value in health.items():
            print(f"{key}: {value}")

        print("\n✅ Test completed successfully!")
        return 0

    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())