# AI-Driven Legal Document Analysis System

Design and implement an AI-driven legal document analysis system that identifies and classifies risky clauses in contracts.

## 🚀 Getting Started

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

## 📁 Project Structure

- `app.py`: Main Streamlit application.
- `src/`: Core logic modules.
    - `extract.py`: PDF text extraction.
    - `clause_splitter.py`: Segmenting text into clauses.
    - `predict.py`: Risk classification logic.
    - `preprocess.py`: Text cleaning utilities.
- `requirements.txt`: Project dependencies.

## 👥 Karan's Task: Application & UI Development
- Streamlit UI for PDF upload.
- Risk Dashboard (High Risk -> Red, Low Risk -> Green).
- End-to-end integration of extraction and prediction.
