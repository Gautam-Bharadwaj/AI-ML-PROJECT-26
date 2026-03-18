import joblib
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("LegalAgent.ML")

class LegalMLModel:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'risk_model.pkl')
