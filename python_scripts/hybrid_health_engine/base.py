from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
import numpy as np

class ProgressStatus(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

@dataclass
class ProjectPhase:
    name: str
    sequence: int
    expected_duration_days: int
    dependencies: List[str]

@dataclass
class PhysicalProgress:
    phase: str
    completeness: float
    confidence: float
    last_updated: datetime
    raw_metrics: Dict[str, float]

@dataclass
class DigitalProgress:
    total_story_points: int
    completed_points: int
    sprint_velocity: float
    commit_frequency: float
    pr_merge_rate: float
    last_updated: datetime

@dataclass
class FusedMetrics:
    true_progress_percentage: float
    predicted_ecd: datetime
    variance_alert: ProgressStatus
    confidence_score: float
    cost_performance_index: float

class BaseEngine(ABC):
    """Base class for all engine components"""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the engine and load any required models/configurations"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate the engine's current state and configurations"""
        pass

    @abstractmethod
    def get_health_metrics(self) -> Dict[str, Union[float, str]]:
        """Return the engine's health metrics"""
        pass

class DataIngestorInterface(ABC):
    """Base interface for data ingestion components"""

    @abstractmethod
    async def fetch_data(self) -> Dict:
        """Fetch data from the source"""
        pass

    @abstractmethod
    async def validate_data(self, data: Dict) -> bool:
        """Validate the fetched data"""
        pass

    @abstractmethod
    async def preprocess_data(self, data: Dict) -> Dict:
        """Preprocess the data before ingestion"""
        pass

class ModelInterface(ABC):
    """Base interface for ML models"""

    @abstractmethod
    def load_model(self, model_path: str) -> bool:
        """Load a trained model from disk"""
        pass

    @abstractmethod
    def predict(self, input_data: Union[np.ndarray, Dict]) -> Dict:
        """Make predictions using the loaded model"""
        pass

    @abstractmethod
    def evaluate(self, test_data: Dict) -> Dict[str, float]:
        """Evaluate model performance on test data"""
        pass

class DashboardMetrics:
    """Class for computing and tracking dashboard metrics"""

    def __init__(self):
        self.metrics_history: List[FusedMetrics] = []

    def add_metrics(self, metrics: FusedMetrics):
        """Add new metrics to history"""
        self.metrics_history.append(metrics)

    def get_trend(self, metric_name: str, window_size: int = 10) -> List[float]:
        """Get trend data for a specific metric"""
        if not self.metrics_history:
            return []
        
        values = []
        for metrics in self.metrics_history[-window_size:]:
            value = getattr(metrics, metric_name, None)
            if value is not None:
                values.append(float(value) if isinstance(value, (int, float)) else 0.0)
        return values

    def get_latest_metrics(self) -> Optional[FusedMetrics]:
        """Get the most recent metrics"""
        return self.metrics_history[-1] if self.metrics_history else None

    def calculate_velocity_trend(self) -> float:
        """Calculate the trend in progress velocity"""
        progress_trend = self.get_trend('true_progress_percentage')
        if len(progress_trend) < 2:
            return 0.0
        
        return np.mean(np.diff(progress_trend))