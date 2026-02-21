import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except (LookupError, AttributeError):
    nltk.download('stopwords')
    nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]
    
    return " ".join(tokens)

def preprocess_dataframe(df, text_col='clause_text'):
    print(f"-> Processing {len(df)} rows...")
    df['cleaned_text'] = df[text_col].apply(clean_text)
    return df
