import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

class Config:
    """Configuration manager for the Hybrid Health Engine"""
    
    def __init__(self):
        # Load environment variables
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        # Base paths
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / 'data'
        self.models_dir = self.base_dir / 'models'
        
        # Create required directories
        self._create_directories()
        
        # Load configurations
        self.jira_config = self._load_jira_config()
        self.github_config = self._load_github_config()
        self.firebase_config = self._load_firebase_config()
        self.cv_config = self._load_cv_config()
        self.phase_weights = self._load_phase_weights()
        self.system_config = self._load_system_config()
        
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        dirs = [
            self.data_dir,
            self.data_dir / 'images',
            self.data_dir / 'drone',
            self.models_dir,
            self.base_dir / '.cache'
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def _load_jira_config(self) -> Dict:
        """Load Jira configuration"""
        return {
            'url': os.getenv('JIRA_URL'),
            'username': os.getenv('JIRA_USERNAME'),
            'api_token': os.getenv('JIRA_API_TOKEN'),
            'project_key': os.getenv('JIRA_PROJECT_KEY')
        }
        
    def _load_github_config(self) -> Dict:
        """Load GitHub configuration"""
        return {
            'token': os.getenv('GITHUB_TOKEN'),
            'repo': os.getenv('GITHUB_REPO')
        }
        
    def _load_firebase_config(self) -> Dict:
        """Load Firebase configuration"""
        return {
            'api_key': os.getenv('FIREBASE_API_KEY'),
            'project_id': os.getenv('FIREBASE_PROJECT_ID'),
            'storage_bucket': os.getenv('FIREBASE_STORAGE_BUCKET')
        }
        
    def _load_cv_config(self) -> Dict:
        """Load Computer Vision configuration"""
        return {
            'model_path': self.models_dir / os.getenv('CV_MODEL_PATH', 'model.pth'),
            'model_type': os.getenv('CV_MODEL_TYPE', 'detection'),
            'input_size': int(os.getenv('IMAGE_INPUT_SIZE', '512'))
        }
        
    def _load_phase_weights(self) -> Dict:
        """Load phase weights configuration"""
        return {
            'foundation': float(os.getenv('FOUNDATION_WEIGHT', '0.2')),
            'framing': float(os.getenv('FRAMING_WEIGHT', '0.3')),
            'exterior': float(os.getenv('EXTERIOR_WEIGHT', '0.2')),
            'interior': float(os.getenv('INTERIOR_WEIGHT', '0.2')),
            'finishing': float(os.getenv('FINISHING_WEIGHT', '0.1'))
        }
        
    def _load_system_config(self) -> Dict:
        """Load system configuration"""
        return {
            'debug': os.getenv('DEBUG_MODE', 'False').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'async_workers': int(os.getenv('ASYNC_WORKERS', '4')),
            'variance_thresholds': {
                'yellow': float(os.getenv('VARIANCE_YELLOW_THRESHOLD', '0.15')),
                'red': float(os.getenv('VARIANCE_RED_THRESHOLD', '0.25'))
            }
        }
        
    def validate(self) -> bool:
        """Validate the configuration"""
        required_vars = [
            self.jira_config['url'],
            self.jira_config['api_token'],
            self.github_config['token'],
            self.firebase_config['api_key']
        ]
        
        return all(required_vars)

# Create a global config instance
config = Config()