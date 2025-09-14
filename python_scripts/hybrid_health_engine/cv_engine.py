from pathlib import Path
from typing import Dict, List, Tuple, Union
import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms

from .base import BaseEngine, ModelInterface, PhysicalProgress

class CVEngine(BaseEngine, ModelInterface):
    """Computer Vision Engine for analyzing physical project progress"""

    def __init__(self, model_config: Dict[str, str]):
        self.model: nn.Module = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_config = model_config
        self.phase_thresholds = {
            "foundation": 0.85,
            "framing": 0.75,
            "exterior": 0.80,
            "interior": 0.70,
            "finishing": 0.90
        }
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])

    def initialize(self) -> bool:
        """Initialize the CV engine and load the model"""
        try:
            self.load_model(self.model_config["model_path"])
            return True
        except Exception as e:
            print(f"Error initializing CV engine: {e}")
            return False

    def validate(self) -> bool:
        """Validate the CV engine's state"""
        return self.model is not None and hasattr(self.model, 'eval')

    def get_health_metrics(self) -> Dict[str, Union[float, str]]:
        """Get CV engine health metrics"""
        return {
            "model_loaded": self.model is not None,
            "device": str(self.device),
            "input_size": "512x512",
            "model_type": self.model_config.get("type", "unknown")
        }

    def load_model(self, model_path: str) -> bool:
        """Load the pre-trained CV model"""
        try:
            model_path = Path(model_path)
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")

            self.model = torch.load(model_path, map_location=self.device)
            self.model.eval()
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def preprocess_image(self, image_path: Union[str, Path, np.ndarray]) -> torch.Tensor:
        """Preprocess an image for model input"""
        if isinstance(image_path, (str, Path)):
            image = cv2.imread(str(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = image_path

        tensor = self.transform(image)
        return tensor.unsqueeze(0).to(self.device)

    def detect_project_phase(self, features: torch.Tensor) -> Tuple[str, float]:
        """Detect the current project phase and its completion percentage"""
        with torch.no_grad():
            phase_scores = self.model(features)
            phase_probs = torch.softmax(phase_scores, dim=1)
            max_prob, phase_idx = torch.max(phase_probs, dim=1)
            
            # Map index to phase name (implement based on your model's classes)
            phases = ["foundation", "framing", "exterior", "interior", "finishing"]
            current_phase = phases[phase_idx.item()]
            
            return current_phase, max_prob.item()

    def analyze_completeness(self, image_features: torch.Tensor) -> float:
        """Analyze the completeness of the current phase"""
        # This would use a separate segmentation head or detection model
        # to analyze the detail-level completeness
        with torch.no_grad():
            completeness_score = self.model.completeness_head(image_features)
            return torch.sigmoid(completeness_score).item()

    def predict(self, input_data: Union[str, np.ndarray, Dict]) -> Dict:
        """Process an image and predict physical progress"""
        try:
            # Preprocess image
            if isinstance(input_data, dict):
                image_path = input_data["image_path"]
            else:
                image_path = input_data
            
            image_tensor = self.preprocess_image(image_path)
            
            # Get phase and confidence
            phase, confidence = self.detect_project_phase(image_tensor)
            
            # Analyze completeness for the detected phase
            completeness = self.analyze_completeness(image_tensor)
            
            # Adjust completeness based on confidence and phase thresholds
            adjusted_completeness = completeness * confidence
            if adjusted_completeness < self.phase_thresholds[phase]:
                adjusted_completeness *= 0.9  # Apply penalty for low confidence
            
            return {
                "phase": phase,
                "completeness": adjusted_completeness,
                "confidence": confidence,
                "raw_metrics": {
                    "unadjusted_completeness": completeness,
                    "phase_threshold": self.phase_thresholds[phase]
                }
            }
        except Exception as e:
            print(f"Error in CV prediction: {e}")
            return None

    def evaluate(self, test_data: Dict) -> Dict[str, float]:
        """Evaluate model performance on test data"""
        if not self.validate():
            return {"error": "Model not properly initialized"}

        total_samples = len(test_data["images"])
        correct_phases = 0
        mae_completeness = 0.0

        for img_path, ground_truth in zip(test_data["images"], test_data["labels"]):
            prediction = self.predict(img_path)
            if prediction["phase"] == ground_truth["phase"]:
                correct_phases += 1
            mae_completeness += abs(prediction["completeness"] - ground_truth["completeness"])

        return {
            "phase_accuracy": correct_phases / total_samples,
            "completeness_mae": mae_completeness / total_samples
        }