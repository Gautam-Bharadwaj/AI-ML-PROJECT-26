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
    st.markdown("## 📡 Uplink Terminal")
    uploaded_file = st.file_uploader("Load PDF Data stream", type="pdf")
    
    if uploaded_file:
        st.success("Data stream synchronized.")
        
    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.9rem; color: #8b949e; line-height: 1.4;">
            <p><strong>MISSION:</strong> Identify high-priority risks and anomalies in legal structures.</p>
            <p><strong>STATUS:</strong> Neural Network Active</p>
        </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    # Save file temporarily
    temp_path = "temp_contract.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    with st.spinner("⚡ Initializing Neural Core and Parsing Data Streams..."):
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
    st.markdown("### 📊 Neural Risk Analysis Dashboard")
    df = pd.DataFrame(results)
    
    col1, col2, col3 = st.columns(3)
    total_clauses = len(df)
    high_risk_count = len(df[df['label'] == "High Risk"])
    low_risk_count = total_clauses - high_risk_count
    
    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <p style='color: #8b949e; font-size: 0.9rem;'>Total Data Segments</p>
                <h2 style='color: #58a6ff;'>{total_clauses}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="glass-card" style="border-top: 2px solid #ff4b4b;">
                <p style='color: #8b949e; font-size: 0.9rem;'>High-Risk Anomalies</p>
                <h2 style='color: #ff4b4b;'>{high_risk_count}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="glass-card" style="border-top: 2px solid #28a745;">
                <p style='color: #8b949e; font-size: 0.9rem;'>Safe Protocols</p>
                <h2 style='color: #28a745;'>{low_risk_count}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed Analysis
    st.markdown("### 🔍 Deep Core Analysis")
    
    for _, row in df.iterrows():
        st_class = "high-risk" if row['label'] == "High Risk" else "low-risk"
        icon = "🔴" if row['label'] == "High Risk" else "🟢"
        
        st.markdown(f"""
            <div class="glass-card {st_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; letter-spacing: 0.1em; color: #58a6ff;">{icon} {row['label'].upper()}</span>
                    <span class="risk-score" style="color: #8b949e;">INITIATING PROBABILITY: {row['score']:.2f}</span>
                </div>
                <div style="margin-top: 15px; color: #d1d5db; line-height: 1.6;">
                    {row['clause']}
                </div>
                <div style="margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                    <span style="font-size: 0.8rem; color: #8b949e; font-style: italic;">AI Insight: This segment contains patterns typical of {row['label'].lower()} scenarios.</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="glass-card" style="text-align: center; border: 1px dashed rgba(255,255,255,0.2);">
            <p style="color: #8b949e; font-size: 1.1rem;">Waiting for PDF Data Stream Uplink...</p>
            <p style="color: #484f58; font-size: 0.9rem;">Please upload a contract via the Sidebar Terminal.</p>
        </div>
    """, unsafe_allow_html=True)