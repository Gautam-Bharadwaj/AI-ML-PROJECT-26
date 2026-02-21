import streamlit as st
import os
import pandas as pd
from src.extract import extract_text_from_pdf
from src.clause_splitter import split_into_clauses
from src.predict import predict_risk

st.set_page_config(page_title="Contract Risk Analyzer", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .high-risk {
        background-color: #ff4b4b22;
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .low-risk {
        background-color: #28a74522;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚖️ AI Legal Document Risk Analysis")
st.markdown("---")

with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF contract", type="pdf")
    
    if uploaded_file:
        st.success("File uploaded successfully!")
        
    st.markdown("---")
    st.info("This tool identifies potential risks in legal contracts using AI-driven analysis.")

if uploaded_file:
    # Save file temporarily
    temp_path = "temp_contract.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    with st.spinner("Extracting text and analyzing clauses..."):
        text = extract_text_from_pdf(temp_path)
        clauses = split_into_clauses(text)
        
        results = []
        for clause in clauses:
            label, score = predict_risk(clause)
            results.append({
                "clause": clause,
                "label": label,
                "score": score
            })
            
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Risk Dashboard
    st.subheader("📊 Risk Assessment Dashboard")
    df = pd.DataFrame(results)
    
    col1, col2, col3 = st.columns(3)
    total_clauses = len(df)
    high_risk_count = len(df[df['label'] == "High Risk"])
    low_risk_count = total_clauses - high_risk_count
    
    col1.metric("Total Clauses", total_clauses)
    col2.metric("High Risk Identified", high_risk_count, delta_color="inverse")
    col3.metric("Low Risk Identified", low_risk_count)
    
    st.markdown("---")
    
    # Detailed Analysis
    st.subheader("🔍 Detailed Clause Analysis")
    
    for _, row in df.iterrows():
        st_class = "high-risk" if row['label'] == "High Risk" else "low-risk"
        color = "#ff4b4b" if row['label'] == "High Risk" else "#28a745"
        
        st.markdown(f"""
            <div class="{st_class}">
                <p style="color: {color}; font-weight: bold; margin-bottom: 5px;">
                    {row['label'].upper()} (Confidence: {row['score']:.2f})
                </p>
                <p style="color: #333;">{row['clause']}</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("Please upload a contract PDF to begin the analysis.")