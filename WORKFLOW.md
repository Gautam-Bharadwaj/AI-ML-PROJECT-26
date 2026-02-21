# Project Workflow & Architecture

This document describes the flow of information and processing steps in the Intelligent Contract Risk Analysis system using Mermaid diagrams.

## 1. High-Level System Architecture
This diagram shows how the user interacts with the system and how the background processes handle the data.

```mermaid
graph TD
    User([User/Legal Professional]) -->|Uploads PDF| UI[Streamlit Interface]
    UI -->|Sends PDF| Extractor[PDF Text Extractor]
    Extractor -->|Raw Text| Splitter[Clause Splitter]
    Splitter -->|Individual Clauses| Preprocessor[Text Preprocessor]
    Preprocessor -->|Cleaned Text| Classifier[Risk Classifier Model]
    Classifier -->|Predicted Risk Levels| UI
    UI -->|Displays Results| User
```

## 2. Milestone 1: Detailed Data Pipeline
This flow represents the work completed for the initial ML-based classification.

```mermaid
flowchart LR
    A[Contract PDF] --> B(PyMuPDF Extraction)
    B --> C{Text Available?}
    C -->|Yes| D[Regex Clause Splitting]
    C -->|No| E[Error Handling]
    D --> F[NLTK Preprocessing]
    F --> G[TF-IDF Vectorization]
    G --> H[ML Model Prediction]
    H --> I[Risk Category Output]
```

## 3. Milestone 2: Agentic Assistant Flow (Upcoming)
This shows how LangGraph and LLMs will interact for deeper legal reasoning.

```mermaid
stateDiagram-v2
    [*] --> InputReceived
    InputReceived --> ExtractingTerms
    ExtractingTerms --> ClassifyingRisk
    ClassifyingRisk --> RiskDetected: High/Medium Risk
    ClassifyingRisk --> LowRisk: Safe
    RiskDetected --> LLM_Analysis: Ask LLM for Explanation
    LLM_Analysis --> SuggestingMitigation: How to fix the clause?
    SuggestingMitigation --> FinalReport
    LowRisk --> FinalReport
    FinalReport --> [*]
```

## 4. Work Division Map
How the team is contributing to the project.

```mermaid
mindmap
  root((Project 26))
    Kumar Gautam
      Data Engineering
      PDF Extraction
      Preprocessing
    Mohit Kourav
      ML Training
      Risk Prediction
      LLM Integration
    Karan Thakur
      Streamlit UI
      Risk Visualization
      Report Generation
```
