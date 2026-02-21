import joblib
import os

def load_predictor():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'risk_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found. Please train the model first.")
    
    return joblib.load(model_path)

def predict_risk(text):
    model = load_predictor()
    if isinstance(text, str):
        text = [text]
    
    prediction = model.predict(text)
    probabilities = model.predict_proba(text)
