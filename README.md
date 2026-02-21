# AI-Driven Legal Document Analysis System

Design and implement an AI-driven legal document analysis system that identifies and classifies risky clauses in contracts.

##  Getting Started

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Project Roadmap
- [x] Directory structure setup (Kumar Gautam)
- [x] Basic text cleaning logic (Kumar Gautam)
- [x] Clause splitting methods (Kumar Gautam)
- [x] PDF text extraction helpers (Kumar Gautam)
- [x] Automated data preparation script (Kumar Gautam)
- [x] ML Model Training & Pipeline (Mohit Kourav)
    - [x] TF-IDF Vectorization logic
    - [x] RandomForest Classification model
    - [x] Model persistence (saving to .pkl)
    - [x] Risk prediction utility
- [x] Building the Streamlit interface (Karan Thakur)
    - [x] HUD-inspired UI Design (Succesship style)
    - [x] PDF Upload & Automated Extraction integration
    - [x] Visual Risk Assessment Matrix (Clause-by-Clause)
    - [x] Real-time Risk Telemetry & Metrics

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
