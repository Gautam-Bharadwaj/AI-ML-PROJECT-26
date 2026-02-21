import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def train_and_save_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_legal_clauses.csv')
    
    df = pd.read_csv(data_path)
    df.dropna(subset=['cleaned_text', 'clause_status'], inplace=True)
    
    X = df['cleaned_text']
    y = df['clause_status'].astype(int)
