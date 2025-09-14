from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from sklearn.ensemble import RandomForestRegressor

from .base import (
    BaseEngine, DigitalProgress, PhysicalProgress, 
    FusedMetrics, ProgressStatus
)

class FusionEngine(BaseEngine):
    """Core fusion engine for combining digital and physical progress metrics"""

    def __init__(self, config: Dict):
        self.config = config
        self.phase_weights = config.get("phase_weights", {
            "foundation": 0.2,
            "framing": 0.3,
            "exterior": 0.2,
            "interior": 0.2,
            "finishing": 0.1
        })
        self.variance_thresholds = config.get("variance_thresholds", {
            "yellow": 0.15,  # 15% variance triggers yellow alert
            "red": 0.25      # 25% variance triggers red alert
        })
        self.ml_model = RandomForestRegressor(n_estimators=100)
        self.historical_data: List[Dict] = []
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the fusion engine"""
        try:
            self.historical_data = []
            self.initialized = True
            return True
        except Exception as e:
            print(f"Error initializing fusion engine: {e}")
            return False

    def validate(self) -> bool:
        """Validate the engine's state"""
        return self.initialized

    def get_health_metrics(self) -> Dict[str, float]:
        """Get fusion engine health metrics"""
        return {
            "data_points": len(self.historical_data),
            "avg_variance": np.mean([d["variance"] for d in self.historical_data]) if self.historical_data else 0.0,
            "model_confidence": self._calculate_model_confidence()
        }

    def _calculate_model_confidence(self) -> float:
        """Calculate the confidence score for the fusion model"""
        if len(self.historical_data) < 10:
            return len(self.historical_data) / 10  # Linear scaling up to 10 data points
        
        # Calculate based on prediction accuracy if we have enough data
        accuracies = [
            1 - abs(d["predicted_progress"] - d["actual_progress"]) / d["actual_progress"]
            for d in self.historical_data[-10:]
            if d.get("actual_progress", 0) > 0
        ]
        return np.mean(accuracies) if accuracies else 0.0

    def calculate_true_ecd(
        self,
        digital_data: DigitalProgress,
        physical_data: PhysicalProgress,
        target_date: datetime,
        historical_ecds: Optional[List[datetime]] = None
    ) -> Tuple[datetime, float]:
        """
        Calculate the true Expected Completion Date (ECD) based on both digital and physical progress.
        This is the core function implementing the "physical bottleneck" rule.
        """
        # Calculate base velocities
        digital_velocity = digital_data.sprint_velocity  # Story points per sprint
        physical_velocity = self._calculate_physical_velocity(physical_data)  # % per day

        # Apply the physical bottleneck rule
        physical_remaining = 1.0 - physical_data.completeness
        digital_remaining = (
            digital_data.total_story_points - digital_data.completed_points
        ) / digital_data.total_story_points

        # The physical progress acts as a bottleneck
        effective_remaining = max(physical_remaining, digital_remaining)
        
        # Calculate days needed based on the slower velocity
        days_needed_physical = physical_remaining / physical_velocity if physical_velocity > 0 else float('inf')
        days_needed_digital = digital_remaining / (digital_velocity / 10) if digital_velocity > 0 else float('inf')
        
        # Take the maximum (bottleneck)
        days_needed = max(days_needed_physical, days_needed_digital)
        
        # Calculate confidence based on multiple factors
        confidence = self._calculate_completion_confidence(
            digital_data,
            physical_data,
            days_needed,
            target_date
        )

        # Adjust prediction with historical trends if available
        if historical_ecds and len(historical_ecds) > 2:
            historical_shift = np.mean([
                (actual - predicted).days
                for predicted, actual in zip(historical_ecds[:-1], historical_ecds[1:])
            ])
            days_needed += historical_shift * (1 - confidence)  # Apply shift based on confidence

        predicted_ecd = datetime.now() + timedelta(days=days_needed)
        
        return predicted_ecd, confidence

    def _calculate_physical_velocity(self, physical_data: PhysicalProgress) -> float:
        """Calculate the velocity of physical progress"""
        # Weight the completeness by phase importance
        weighted_completeness = physical_data.completeness * self.phase_weights.get(
            physical_data.phase, 0.2
        )
        
        # Adjust velocity based on confidence
        return weighted_completeness * physical_data.confidence

    def calculate_progress_variance(
        self,
        digital_progress: float,
        physical_progress: float
    ) -> Tuple[float, ProgressStatus]:
        """Calculate variance between reported and actual progress"""
        variance = abs(digital_progress - physical_progress)
        
        # Determine status based on variance thresholds
        if variance >= self.variance_thresholds["red"]:
            status = ProgressStatus.RED
        elif variance >= self.variance_thresholds["yellow"]:
            status = ProgressStatus.YELLOW
        else:
            status = ProgressStatus.GREEN
            
        return variance, status

    def calculate_cost_performance_index(
        self,
        planned_value: float,
        earned_value: float,
        actual_cost: float
    ) -> float:
        """Calculate Cost Performance Index (CPI)"""
        if actual_cost == 0:
            return 1.0
        
        return earned_value / actual_cost

    def _calculate_completion_confidence(
        self,
        digital_data: DigitalProgress,
        physical_data: PhysicalProgress,
        predicted_days: float,
        target_date: datetime
    ) -> float:
        """Calculate the confidence score for completion prediction"""
        # Base confidence from physical progress
        confidence = physical_data.confidence

        # Adjust based on variance between digital and physical progress
        digital_progress = digital_data.completed_points / digital_data.total_story_points
        variance_factor = 1 - abs(digital_progress - physical_data.completeness)
        confidence *= variance_factor

        # Adjust based on time pressure
        days_to_target = (target_date - datetime.now()).days
        if days_to_target > 0:
            time_pressure = predicted_days / days_to_target
            confidence *= 1 / (1 + max(0, time_pressure - 1))

        # Adjust based on sprint velocity stability
        if digital_data.sprint_velocity > 0:
            velocity_stability = min(
                1.0,
                digital_data.pr_merge_rate * digital_data.commit_frequency / 5.0
            )
            confidence *= velocity_stability

        return max(0.0, min(1.0, confidence))

    def fuse_progress_data(
        self,
        digital_data: DigitalProgress,
        physical_data: PhysicalProgress,
        target_date: datetime,
        budget_data: Dict[str, float]
    ) -> FusedMetrics:
        """
        Fuse digital and physical progress data to create unified metrics.
        This is the main entry point for the fusion engine.
        """
        # Calculate true progress based on physical bottleneck
        digital_progress = digital_data.completed_points / digital_data.total_story_points
        physical_progress = physical_data.completeness
        
        # Physical progress acts as a bottleneck
        true_progress = min(digital_progress, physical_progress)
        
        # Calculate variance and status
        variance, variance_alert = self.calculate_progress_variance(
            digital_progress, physical_progress
        )
        
        # Calculate predicted completion date and confidence
        predicted_ecd, confidence_score = self.calculate_true_ecd(
            digital_data, physical_data, target_date
        )
        
        # Calculate CPI
        planned_value = budget_data["budget"] * digital_progress
        earned_value = budget_data["budget"] * true_progress
        cpi = self.calculate_cost_performance_index(
            planned_value, earned_value, budget_data["actual_cost"]
        )
        
        # Create fused metrics
        metrics = FusedMetrics(
            true_progress_percentage=true_progress * 100,
            predicted_ecd=predicted_ecd,
            variance_alert=variance_alert,
            confidence_score=confidence_score,
            cost_performance_index=cpi
        )
        
        # Update historical data for future predictions
        self.historical_data.append({
            "timestamp": datetime.now(),
            "digital_progress": digital_progress,
            "physical_progress": physical_progress,
            "variance": variance,
            "predicted_progress": true_progress,
            "actual_progress": true_progress  # Will be updated later if actual differs
        })
        
        return metrics