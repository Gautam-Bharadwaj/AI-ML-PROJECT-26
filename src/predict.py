import re

def predict_risk(clause_text):
    high_risk_keywords = [
        "terminate", "liability", "indemnity", "breach", "penalty", 
        "governing law", "arbitration", "confidential", "warranty",
        "force majeure", "limitation", "exclusive"
    ]
    
    text_lower = clause_text.lower()
    
    for kw in high_risk_keywords:
        if re.search(rf"\b{kw}\b", text_lower):
            return "High Risk", 0.85
            
    return "Low Risk", 0.15
