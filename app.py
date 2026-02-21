import streamlit as st
import os
import pandas as pd
from src.extract import extract_text_from_pdf
from src.clause_splitter import split_into_clauses
from src.predict import predict_risk

# Page Configuration
st.set_page_config(page_title="Contract Intelligence Unit", page_icon="⚡", layout="wide")

# Theme: Deep Blacks, Glowing Accents, Glassmorphism
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;600;800&family=JetBrains+Mono&display=swap');

/* Global Styles */
.stApp {
    background-color: #000000;
    color: #FFFFFF;
    font-family: 'Geist', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Glass Container */
.glass-container {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 24px;
    backdrop-filter: blur(10px);
}

/* Typography */
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1;
    margin-bottom: 16px;
    background: linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0.5) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 48px;
}

.label-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.2rem;
    color: #58A6FF;
    margin-bottom: 8px;
    display: block;
}

/* Bento Cards */
.bento-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 24px;
    height: 100%;
    transition: all 0.3s ease;
}

.bento-card:hover {
    border-color: rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.08);
}

/* Risk Indicators */
.risk-tag {
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}
.risk-high { background: rgba(255, 59, 48, 0.1); color: #FF3B30; border: 1px solid rgba(255, 59, 48, 0.2); }
.risk-low { background: rgba(52, 199, 89, 0.1); color: #34C759; border: 1px solid rgba(52, 199, 89, 0.2); }

/* Custom Sidebar */
[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Custom File Uploader Style */
.stFileUploader section {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 2px dashed rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    padding: 40px !important;
}

.stFileUploader section:hover {
    border-color: #58A6FF !important;
}
</style>
""", unsafe_allow_html=True)

# Main UI Layout
st.markdown('<span class="label-mono">Powered by Agentic Intelligence</span>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Automate Legal<br>Risk Analysis.</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Upload complex contracts and identify high-risk clauses in seconds, instantly.</p>', unsafe_allow_html=True)

# Sidebar - Uplink Terminal
with st.sidebar:
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Uplink Terminal</span>', unsafe_allow_html=True)
    st.markdown('<h3 style="font-weight:700;">Data Ingestion</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop PDF", type="pdf", label_visibility="collapsed")
    
    if uploaded_file:
        st.markdown('<div class="risk-tag risk-low" style="text-align:center;">UPLINK_SUCCESSFUL</div>', unsafe_allow_html=True)
    
    st.markdown('<br>' * 10, unsafe_allow_html=True)
    st.markdown('<span class="label-mono">System Status</span>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.8rem; color:rgba(255,255,255,0.4);">Core Engine: Active<br>Latency: 42ms<br>Version: 2.0.1</p>', unsafe_allow_html=True)

# Logic Section
if uploaded_file:
    temp_name = "active_contract.pdf"
    with open(temp_name, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    with st.spinner("Processing Data Streams..."):
        full_text = extract_text_from_pdf(temp_name)
        clause_list = split_into_clauses(full_text)
        
        # Batch prediction
        processed_data = []
        for c in clause_list:
            pred = predict_risk(c)[0]
            processed_data.append({
                "clause": c,
                "is_risky": pred['is_risky'],
                "confidence": pred['risk_probability']
            })
            
    if os.path.exists(temp_name):
        os.remove(temp_name)

    # Dashboard Metrics (Bento Style)
    st.markdown('<span class="label-mono">Intelligence Report</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    risky_count = sum(1 for x in processed_data if x['is_risky'])
    
    with col1:
        st.markdown(f"""
            <div class="bento-card">
                <span class="label-mono">Analysis Scope</span>
                <h2 style="font-size:2.5rem; font-weight:800; margin-top:10px;">{len(processed_data)}</h2>
                <p style="color:rgba(255,255,255,0.4); font-size:0.8rem;">TOTAL_CLAUSES</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="bento-card">
                <span class="label-mono" style="color:#FF3B30;">Anomalies</span>
                <h2 style="font-size:2.5rem; font-weight:800; color:#FF3B30; margin-top:10px;">{risky_count}</h2>
                <p style="color:rgba(255,100,100,0.4); font-size:0.8rem;">RISKY_CLAUSES_DETECTED</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="bento-card">
                <span class="label-mono" style="color:#34C759;">Integrity</span>
                <h2 style="font-size:2.5rem; font-weight:800; color:#34C759; margin-top:10px;">{int((len(processed_data)-risky_count)/len(processed_data)*100)}%</h2>
                <p style="color:rgba(100,255,100,0.4); font-size:0.8rem;">SAFE_SYMBOLS_RATIO</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Detailed Clause Audit</span>', unsafe_allow_html=True)

    # Detailed Clause List
    for i, item in enumerate(processed_data):
        risk_class = "risk-high" if item['is_risky'] else "risk-low"
        risk_text = "DANGER / HIGH RISK" if item['is_risky'] else "NOMINAL / LOW RISK"
        
        st.markdown(f"""
            <div class="glass-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <span class="risk-tag {risk_class}">{risk_text}</span>
                    <span class="label-mono" style="opacity:0.5;">ID: C-{i+1:03} | CONF: {item['confidence']:.2%}</span>
                </div>
                <div style="font-size:1.1rem; color:#E1E4E8; line-height:1.6;">
                    {item['clause']}
                </div>
            </div>
        """, unsafe_allow_html=True)

else:
    # Empty State - Call to Action
    st.markdown('<br>' * 2, unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; padding: 120px 40px; border: 1px solid rgba(255,255,255,0.05); border-radius: 40px; background: radial-gradient(circle at center, rgba(88, 166, 255, 0.05) 0%, transparent 70%);">
            <h2 style="font-weight:600; font-size:2rem;">Ready to automate?</h2>
            <p style="color:rgba(255,255,255,0.4); margin-bottom:32px;">Drag and drop your contract PDF to the side terminal to begin the audit.</p>
        </div>
    """, unsafe_allow_html=True)