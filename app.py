import streamlit as st
import os
import pandas as pd
from src.extract import extract_text_from_pdf
from src.clause_splitter import split_into_clauses
from src.predict import predict_risk

st.set_page_config(page_title="Contract Risk Analyzer", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #010409 100%);
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .high-risk {
        border-left: 4px solid #ff4b4b;
        background: linear-gradient(90deg, rgba(255, 75, 75, 0.1) 0%, rgba(255, 75, 75, 0.02) 100%);
    }
    
    .low-risk {
        border-left: 4px solid #28a745;
        background: linear-gradient(90deg, rgba(40, 167, 69, 0.1) 0%, rgba(40, 167, 69, 0.02) 100%);
    }

    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #58a6ff;
    }
    </style>
""", unsafe_allow_html=True)

st.image("/Users/karanthakur/.gemini/antigravity/brain/d5dfa2a2-627e-4317-a1a2-c378ff4115a4/futuristic_legal_header_bg_1771669071836.png", use_container_width=True)
st.title("⚖️ Legal Intelligence Matrix")
st.markdown("<p style='font-size: 1.1rem; color: #8b949e;'>Advanced Risk Assessment & Clause Classification Agent</p>", unsafe_allow_html=True)
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