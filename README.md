# Intelligent Contract Risk Analysis and Agentic Legal Assistance System

## Project Objective
The goal of this project is to design and implement an AI-driven system for analyzing legal documents. The system identifies and classifies risky clauses within contracts and will eventually be expanded into an agentic AI assistant capable of generating structured risk assessments and detailed explanations.

## Team Members
* Kumar Gautam
* Mohit Kourav
* Karan Thakur

## Technical Stack (Milestone 1)
* Language: Python 3.x
* NLP / ML Libraries: scikit-learn, NLTK, spaCy, and PyMuPDF
* Dataset: Kaggle Legal Dataset and IndianKanoon
* User Interface: Streamlit or Gradio
* Hosting: Streamlit Community Cloud or Hugging Face Spaces

## Constraints and Requirements
* No Paid APIs: All components must use free-tier APIs or open-source models.
* Mandatory UI: The final application must include a user interface; local demonstrations are not sufficient.
* Public Hosting: The system must be hosted on a public platform for accessibility.

## Project Roadmap

### Milestone 1: ML-Based Contract Risk Classification (Current)
* Objective: Build a classical NLP and machine learning pipeline to identify potentially risky clauses.
* Status:
    * Text Extraction: Extracting text from PDF and text-based contract documents.
    * Clause Segmentation: Breaking documents down into individual legal provisions.
    * Data Preprocessing: Cleaning text via lowercasing, lemmatization, and stopword removal.
    * Risk Classification: Training models to categorize clauses by their associated risk levels.

### Milestone 2: Agentic AI Assistant (Upcoming)
* Agent Workflow: Utilizing LangGraph for structured legal reasoning and task management.
* LLM Integration: Implementing open-source models to provide natural language explanations of risks.

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Gautam-Bharadwaj/AI-ML-PROJECT-26.git](https://github.com/Gautam-Bharadwaj/AI-ML-PROJECT-26.git)

2. Install the required dependencies:

   ```bash
    pip install pymupdf nltk scikit-learn pandas streamlit

    Launch the application:
```bash
   streamlit run app.py
