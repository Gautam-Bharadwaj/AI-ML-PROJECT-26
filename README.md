# Intelligent Contract Risk Analysis and Agentic Legal Assistance System

## Project Objective
AI-driven system for analyzing legal documents to identify and classify risky clauses.

## Project Structure
```text
.
├── data/               # Project data
│   ├── processed/      # Cleaned data ready for ML
│   └── raw/            # Original PDF/Text contracts
├── models/             # Trained ML models (pkl, joblib)
├── notebooks/          # Jupyter notebooks for exploration
├── src/                # Source code
│   ├── clause_splitter.py
│   ├── predict.py
│   ├── preprocess.py
│   └── train_model.py
├── app.py              # Streamlit Web Interface
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Technical Stack (Milestone 1)
* **Language:** Python 3.x
* **NLP / ML:** scikit-learn, NLTK, spaCy
* **Extraction:** PyMuPDF (fitz)
* **UI:** Streamlit
* **Hosting:** Streamlit Community Cloud

## Milestone 1 Roadmap
- [x] Structure Setup
- [x] Basic Preprocessing Logic
- [x] Clause Segmentation Logic
- [ ] PDF Text Extraction Script
- [ ] Model Training on Kaggle/IndianKanoon Dataset
- [ ] Streamlit UI Implementation

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the App:
   ```bash
   streamlit run app.py
   ```
