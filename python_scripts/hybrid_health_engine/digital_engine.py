from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

from .base import BaseEngine, DigitalProgress

class DigitalVelocityEngine(BaseEngine):
    """Engine for analyzing project management metrics and predicting velocity"""

    def __init__(self):
        self.velocity_model = LinearRegression()
        self.velocity_history: List[float] = []
        self.progress_history: List[Tuple[datetime, float]] = []
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the digital velocity engine"""
        try:
            self.velocity_history = []
            self.progress_history = []
            self.initialized = True
            return True
        except Exception as e:
            print(f"Error initializing digital velocity engine: {e}")
            return False

    def validate(self) -> bool:
        """Validate the engine's state"""
        return self.initialized

    def get_health_metrics(self) -> Dict[str, float]:
        """Get engine health metrics"""
        if not self.velocity_history:
            return {
                "avg_velocity": 0.0,
                "velocity_stability": 0.0,
                "data_points": 0
            }

        return {
            "avg_velocity": np.mean(self.velocity_history),
            "velocity_stability": np.std(self.velocity_history),
            "data_points": len(self.velocity_history)
        }

    def update_progress_history(self, timestamp: datetime, progress: float):
        """Update the progress history with new data point"""
        self.progress_history.append((timestamp, progress))
        self._update_velocity()

    def _update_velocity(self):
        """Calculate and update velocity based on progress history"""
        if len(self.progress_history) < 2:
            return

        # Calculate velocity as progress change per day
        recent_progress = sorted(self.progress_history[-10:])  # Last 10 data points
        progress_changes = []
        time_intervals = []

        for i in range(1, len(recent_progress)):
            time_diff = (recent_progress[i][0] - recent_progress[i-1][0]).days
            progress_diff = recent_progress[i][1] - recent_progress[i-1][1]
            
            if time_diff > 0:  # Avoid division by zero
                progress_changes.append(progress_diff)
                time_intervals.append(time_diff)

        if progress_changes:
            velocity = sum(progress_changes) / sum(time_intervals)
            self.velocity_history.append(velocity)

    def calculate_sprint_metrics(self, sprint_data: Dict) -> Dict[str, float]:
        """Calculate various sprint-based metrics"""
        if not sprint_data.get("completed_sprints"):
            return {
                "avg_velocity": 0.0,
                "completion_rate": 0.0,
                "predictability": 0.0
            }

        velocities = [
            sprint["completed_points"] / sprint["duration_days"]
            for sprint in sprint_data["completed_sprints"]
        ]

        planned_vs_completed = [
            sprint["completed_points"] / sprint["planned_points"]
            for sprint in sprint_data["completed_sprints"]
            if sprint["planned_points"] > 0
        ]

        return {
            "avg_velocity": np.mean(velocities),
            "completion_rate": np.mean(planned_vs_completed),
            "predictability": 1 - np.std(planned_vs_completed)
        }

    def predict_completion(self, 
                         current_progress: DigitalProgress,
                         target_points: int,
                         confidence_level: float = 0.8) -> Dict:
        """Predict project completion based on velocity data"""
        if not self.velocity_history:
            return {
                "predicted_date": None,
                "confidence": 0.0,
                "remaining_points": target_points - current_progress.completed_points
            }

        # Calculate base velocity metrics
        mean_velocity = np.mean(self.velocity_history)
        velocity_std = np.std(self.velocity_history)
        
        # Adjust velocity based on confidence level
        adjusted_velocity = mean_velocity - (velocity_std * (1 - confidence_level))
        
        # Calculate remaining work and time
        remaining_points = target_points - current_progress.completed_points
        predicted_days = remaining_points / max(adjusted_velocity, 0.1)  # Avoid division by zero
        
        # Calculate confidence based on velocity stability and data points
        velocity_stability = 1 - (velocity_std / mean_velocity if mean_velocity > 0 else 1)
        data_confidence = min(len(self.velocity_history) / 10, 1)  # Scale with amount of data
        overall_confidence = velocity_stability * data_confidence * confidence_level

        return {
            "predicted_date": datetime.now() + timedelta(days=predicted_days),
            "confidence": overall_confidence,
            "remaining_points": remaining_points,
            "adjusted_velocity": adjusted_velocity
        }

    def analyze_trends(self, window_size: int = 5) -> Dict[str, float]:
        """Analyze recent trends in velocity and progress"""
        if len(self.velocity_history) < window_size:
            return {
                "velocity_trend": 0.0,
                "acceleration": 0.0,
                "stability_score": 0.0
            }

        recent_velocities = self.velocity_history[-window_size:]
        velocity_changes = np.diff(recent_velocities)

        return {
            "velocity_trend": np.mean(velocity_changes),
            "acceleration": np.mean(velocity_changes) / window_size,
            "stability_score": 1 / (1 + np.std(recent_velocities))
        }

    def get_risk_factors(self, digital_progress: DigitalProgress) -> Dict[str, float]:
        """Calculate risk factors based on digital metrics"""
        risk_factors = {
            "velocity_instability": 0.0,
            "completion_rate_risk": 0.0,
            "resource_utilization_risk": 0.0
        }

        # Velocity instability risk
        if self.velocity_history:
            velocity_std = np.std(self.velocity_history)
            velocity_mean = np.mean(self.velocity_history)
            risk_factors["velocity_instability"] = min(
                velocity_std / (velocity_mean if velocity_mean > 0 else 1), 
                1.0
            )

        # Completion rate risk
        planned_velocity = digital_progress.total_story_points / 100  # Assuming 100 days baseline
        actual_velocity = digital_progress.sprint_velocity
        risk_factors["completion_rate_risk"] = max(
            0, 
            min(1, (planned_velocity - actual_velocity) / planned_velocity if planned_velocity > 0 else 0)
        )

        # Resource utilization risk based on commit frequency and PR merge rate
        expected_commit_freq = 5.0  # Expected commits per day
        expected_merge_rate = 0.8   # Expected PR merge rate
        
        commit_risk = max(0, min(1, (expected_commit_freq - digital_progress.commit_frequency) / expected_commit_freq))
        merge_risk = max(0, min(1, (expected_merge_rate - digital_progress.pr_merge_rate) / expected_merge_rate))
        
        risk_factors["resource_utilization_risk"] = (commit_risk + merge_risk) / 2

        return risk_factors