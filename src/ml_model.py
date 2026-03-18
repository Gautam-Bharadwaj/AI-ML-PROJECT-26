import joblib
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("LegalAgent.ML")

class LegalMLModel:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'risk_model.pkl')
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at {model_path}")
            self.model = None
        else:
            try:
                self.model = joblib.load(model_path)
                logger.info("RandomForest Model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                self.model = None
