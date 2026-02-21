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

## Project Roadmap
- [x] Directory structure setup (Kumar Gautam)
- [x] Basic text cleaning logic (Kumar Gautam)
- [x] Clause splitting methods (Kumar Gautam)
- [x] PDF text extraction helpers (Kumar Gautam)
- [x] Automated data preparation script (Kumar Gautam)
- [ ] Training the ML model (Mohit Kourav)
- [ ] Building the Streamlit interface (Karan Thakur)

## How to Run (Workflow)
1. **Install what's needed:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup the Dataset:**
   Run this to clean your raw data and get it ready for training:
   ```bash
   python3 src/prepare_dataset.py
   ```
   *This will create: `data/processed/cleaned_legal_clauses.csv`*

3. **Launch the App:**
   ```bash
   streamlit run app.py
   ```
