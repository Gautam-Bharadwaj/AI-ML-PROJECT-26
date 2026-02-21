import streamlit as st
import os
import pandas as pd
from src.extract import extract_text_from_pdf
from src.clause_splitter import split_into_clauses
from src.predict import predict_risk

st.set_page_config(page_title="Contract Risk Matrix", page_icon="⚖️", layout="wide")

# Inspiration: Succesship. Clean, off-white, soft glows, HUD-style typography.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {
        background-color: #FAFAFA;
        background-image: radial-gradient(circle at 0% 0%, rgba(88, 166, 255, 0.05) 0%, transparent 50%),
                          radial-gradient(circle at 100% 100%, rgba(88, 166, 255, 0.05) 0%, transparent 50%);
        color: #1F2328;
        font-family: 'Inter', sans-serif;
    }
    
    .stHeader {
        background: transparent;
    }
    
    /* HUD Header styling */
    .hud-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #8b949e;
        margin-bottom: 4px;
    }
    
    .main-title {
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.03em;
        color: #000000;
        margin-top: -10px;
    }
    
    /* Clean Minimalist Cards */
    .status-card {
        background: white;
        border: 1px solid #E1E4E8;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .risk-card {
        background: white;
        border: 1px solid #E1E4E8;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
    }
    
    .risk-high {
        border-left: 4px solid #D73A49;
    }
    
    .risk-low {
        border-left: 4px solid #28A745;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F6F8FA !important;
        border-right: 1px solid #E1E4E8;
    }
    
    .sidebar-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        color: #57606A;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# HUD Header
st.markdown('<p class="hud-label">SYSTEM : LEGAL_INTELLIGENCE_UNIT</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Contract Risk Matrix</h1>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.markdown('<p class="sidebar-label">DATA UPLINK TERMINAL</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
    
    if uploaded_file:
        st.success("SYNC_COMPLETE")
        
    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.8rem; color: #57606A;">
            <p><strong>STATUS:</strong> NOMINAL</p>
            <p><strong>VERSION:</strong> 1.0.2-BETA</p>
        </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    temp_path = "temp_contract.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    with st.spinner("ANALYZING_DATA_STREAMS..."):
        text = extract_text_from_pdf(temp_path)
        clauses = split_into_clauses(text)
        results = [{"clause": c, "label": predict_risk(c)[0], "score": predict_risk(c)[1]} for c in clauses]
            
    if os.path.exists(temp_path):
        os.remove(temp_path)

    df = pd.DataFrame(results)
    high_risk_count = len(df[df['label'] == "High Risk"])
    low_risk_count = len(df) - high_risk_count

    # Metrics HUD
    st.markdown('<p class="hud-label">TELEMETRY : RISK_PROFILE</p>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f'<div class="status-card"><p class="hud-label">TOTAL_SEGMENTS</p><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="status-card"><p class="hud-label" style="color:#D73A49">HIGH_ANOMALIES</p><h2 style="color:#D73A49">{high_risk_count}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="status-card"><p class="hud-label" style="color:#28A745">SAFE_PROTOCOLS</p><h2 style="color:#28A745">{low_risk_count}</h2></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<p class="hud-label">CORE_ANALYSIS : CLAUSE_BY_CLAUSE</p>', unsafe_allow_html=True)
    
    for _, row in df.iterrows():
        r_class = "risk-high" if row['label'] == "High Risk" else "risk-low"
        r_color = "#D73A49" if row['label'] == "High Risk" else "#28A745"
        
        st.markdown(f"""
            <div class="risk-card {r_class}">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-family:'JetBrains Mono', monospace; font-size:0.7rem; font-weight:bold; color:{r_color};">{row['label'].upper()}</span>
                    <span style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#8b949e;">CONFIDENCE: {row['score']:.2f}</span>
                </div>
                <div style="margin-top:12px; font-size:0.95rem; line-height:1.5; color:#24292F;">
                    {row['clause']}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="text-align:center; padding: 100px 0; color: #8b949e;">
            <p class="hud-label">WAITING_FOR_INPUT</p>
            <p style="font-size: 1.1rem;">Load a PDF document into the Uplink Terminal to begin.</p>
        </div>
    """, unsafe_allow_html=True)