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
    
    results = []
    for i in range(len(text)):
        result = {
            'text': text[i],
            'is_risky': bool(prediction[i]),
            'risk_probability': float(probabilities[i][1])
        }
        results.append(result)
        
    return results

if __name__ == '__main__':
    sample_texts = [
        "The company shall not make any investments without prior approval.",
        "We agree to pay the standard fee for the services rendered."
    ]
    predictions = predict_risk(sample_texts)
    for p in predictions:
        print(f"Risk: {p['is_risky']} | Prob: {p['risk_probability']:.2f} | Text: {p['text']}")
