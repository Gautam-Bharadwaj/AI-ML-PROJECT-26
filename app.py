import streamlit as st
import os
import pandas as pd
import numpy as np
import base64
from src.extract import extract_text_from_pdf, extract_legal_metadata
from src.clause_splitter import split_into_clauses
from src.predict import predict_risk
from src.agent_logic import analyze_risk_with_agent
from src.exporter import generate_json_report, generate_pdf_report
from src.database import save_audit
import concurrent.futures
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Page config
st.set_page_config(page_title="Pippo AI | Legal Partner", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cabin+Sketch:wght@400;700&family=Caveat:wght@600;700&family=Inter:wght@400;500;600;700;800&family=Outfit:wght@700;800;900&family=Geist:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #000000 !important;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='1' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
        color: #FFFFFF !important;
        font-family: 'Geist', sans-serif;
        overflow-x: hidden !important;
    }
    
    /* Hide default streamlit elements */
    [data-testid="stHeader"], header { visibility: hidden; height: 0; padding: 0; display: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Remove top padding */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    .stApp { margin-top: 0px !important; }
    
    /* Branding Elements */
    .h-title {
        font-family: 'Cabin Sketch', cursive; 
        font-size: clamp(2.5rem, 12vw, 5.5rem); 
        font-weight: 700; 
        line-height: 0.85;
        letter-spacing: -3px; 
        color: #E91E63; 
        margin-bottom: 25px;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.05);
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

    .hero-subtitle {
        font-family: 'Inter';
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.5);
        margin-bottom: 30px;
        max-width: 600px;
        line-height: 1.5;
    }

    /* Glass Panels */
    .glass-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 32px;
        backdrop-filter: blur(10px);
    }

    .bento-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    .bento-card:hover { border-color: rgba(255, 255, 255, 0.3); background: rgba(255, 255, 255, 0.08); }

    /* Float Animation */
    @keyframes float-pippo {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(1deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }
    .pippo-float { animation: float-pippo 4s ease-in-out infinite; }

    /* Scanning Animation */
    @keyframes scan-glow {
        0% { background-position: -100% 0; opacity: 0.1; }
        50% { opacity: 0.3; }
        100% { background-position: 200% 0; opacity: 0.1; }
    }
    .scanning-overlay {
        background: linear-gradient(90deg, transparent, #58A6FF, transparent);
        background-size: 200% 100%;
        animation: scan-glow 2s infinite linear;
        height: 3px;
        margin-top: 10px;
    }

    /* Agentic Insight Box */
    .agentic-panel {
        background: linear-gradient(135deg, rgba(88, 166, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .agent-title {
        font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #58A6FF;
        display: flex; align-items: center; gap: 8px; text-transform: uppercase; letter-spacing: 0.15rem;
    }
    .agent-text { color: #D1D5DB; font-size: 1rem; line-height: 1.6; margin-top: 15px; }

    .risk-tag {
        padding: 4px 12px; border-radius: 99px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
    }
    .risk-high { background: rgba(255, 59, 48, 0.1); color: #FF3B30; border: 1px solid rgba(255, 59, 48, 0.2); }
    .risk-low { background: rgba(52, 199, 89, 0.1); color: #34C759; border: 1px solid rgba(52, 199, 89, 0.2); }

    .stFileUploader section {
        background: transparent !important; border: 1.5px dashed rgba(88, 166, 255, 0.2) !important; border-radius: 20px !important; padding: 30px !important;
    }
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------
# UI: PIPPO BRANDED NAVBAR
# ---------------------------------------------------------
navbar_html = """<div style="background-color: #E91E63; background-image: repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.08) 0px, rgba(255, 255, 255, 0.08) 1.5px, transparent 1.5px, transparent 12px); width: 100vw; height: 100px; display: flex; align-items: center; justify-content: space-between; padding: 0 5vw; border-bottom: 4px solid #C2185B; position: relative; z-index: 100000; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-top: -60px; margin-left: -5vw;"><div style="display: flex; align-items: flex-end; gap: 10px;"><h1 style="font-family: 'Cabin Sketch', cursive; font-weight: 700; font-size: 3.4rem; color: #FFFFFF !important; margin: 0; letter-spacing: 0px; text-shadow: 3px 3px 0px rgba(0,0,0,0.1); line-height: 1;">Pippo</h1></div><div style="display: flex; align-items: center; gap: 20px;"><div style="background: rgba(255,255,255,0.15); padding: 7px 15px; border-radius: 50px; display: flex; align-items: center; gap: 8px; font-size: 0.72rem; font-weight: 800; color: #FFF; font-family: 'Inter'; border: 1px solid rgba(255,255,255,0.2);"><span style="width:8px; height:8px; background:#00E676; border-radius:50%; box-shadow:0 0 8px #00E676;"></span><span>SYSTEM SECURE</span></div><div style="display: flex; flex-direction: column; text-align: right; line-height: 1; font-family:'Inter'; color:#FFF;"><span style="font-size: 0.6rem; opacity: 0.8; font-weight:800;">AUTHENTICATED</span><span style="font-size: 0.95rem; font-weight: 800;">Gautam Bharadwaj</span></div><div style="width:42px; height:42px; background:#FFF; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.2rem; border:2px solid #FFF; color: #D84315; font-family: sans-serif;">GB</div></div></div>"""
st.markdown(navbar_html, unsafe_allow_html=True)
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN APP AREA
# ---------------------------------------------------------
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown("""
        <div class="h-title">
            <span style="color: #00BFFF; text-shadow: 2px 2px 12px rgba(0,191,255,0.3);">Bharat’s Precision.</span><br>
            <span style="color: #FFFFFF; text-shadow: 2px 2px 12px rgba(255,255,255,0.15);">Global Ambition.</span><br>
            <span style="color: #E91E63; text-shadow: 3px 3px 12px rgba(233,30,99,0.3);">Intellectually</span> 
            <span style="color: #E91E63; text-shadow: 2px 2px 12px rgba(233,30,99,0.3); font-weight: 800;">World.</span>
        </div>
        <p class="hero-subtitle">
            "Architecture matters. While regular trackers skim the surface, Pippo AI is engineered for the deep nuances of Bharat’s legal landscape. We deliver the tactical context you need to win." 🇮🇳
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 40px; border: 1.5px dashed rgba(88, 166, 255, 0.3); border-radius: 20px; padding: 20px; background: rgba(88, 166, 255, 0.02);">', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Uplink Terminal</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop PDF", type="pdf", label_visibility="collapsed")
    if uploaded_file:
        st.markdown('<div class="risk-tag risk-low" style="text-align:center; margin-top: 10px;">UPLINK_SUCCESSFUL</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size: 0.6rem; color: rgba(255,255,255,0.2); margin-top: 8px;">ENCRYPTION_LAYER: ACTIVE // PROTOCOL: LEGAL_MATRIX_V1</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
if uploaded_file:
    temp_name = "active_contract.pdf"
    with open(temp_name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("Initializing Uplink..."):
        st.markdown('<div class="scanning-overlay"></div>', unsafe_allow_html=True)
        full_text = extract_text_from_pdf(temp_name)
        st.markdown('<div class="scanning-overlay"></div>', unsafe_allow_html=True)
        clause_list = split_into_clauses(full_text)
        metadata = extract_legal_metadata(full_text)
        def _process_clause(c):
            pred = predict_risk(c)[0]
            return {
                "clause": c,
                "is_risky": pred['is_risky'],
                "confidence": pred['risk_probability']
            }
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            processed_data = list(executor.map(_process_clause, clause_list))
    if os.path.exists(temp_name):
        os.remove(temp_name)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Contract DNA</span>', unsafe_allow_html=True)
    cols = st.columns(len(metadata))
    for i, (key, val) in enumerate(metadata.items()):
        with cols[i]:
            display_val = ", ".join(val) if isinstance(val, list) and val else (val if val else "NOT_FOUND")
            st.markdown(f"""
                <div class="bento-card" style="padding: 15px;">
                    <span class="label-mono" style="font-size: 0.55rem; opacity: 0.5;">{key}</span>
                    <p style="font-size: 0.9rem; font-weight: 600; margin: 5px 0 0 0; color: #58A6FF;">{display_val}</p>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Intelligence Report</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    risky_count = sum(1 for x in processed_data if x['is_risky'])
    try:
        safe_ratio = (len(processed_data) - risky_count) / len(processed_data) if processed_data else 0
        save_audit(uploaded_file.name, len(processed_data), risky_count, safe_ratio, processed_data)
    except Exception as e:
        print(f"Audit log failed: {e}")
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
                <h2 style="font-size:2.5rem; font-weight:800; color:#34C759; margin-top:10px;">{int((len(processed_data)-risky_count)/len(processed_data)*100) if len(processed_data)>0 else 0}%</h2>
                <p style="color:rgba(100,255,100,0.4); font-size:0.8rem;">SAFE_SYMBOLS_RATIO</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Risk Analytics & Distribution</span>', unsafe_allow_html=True)
    vis_col1, vis_col2 = st.columns([1, 1.2])
    with vis_col1:
        st.markdown('<div class="bento-card" style="height: 400px;">', unsafe_allow_html=True)
        risk_dist = pd.DataFrame({
            "Status": ["Risky", "Safe"],
            "Count": [risky_count, len(processed_data) - risky_count]
        })
        fig_donut = px.pie(
            risk_dist, 
            values="Count", 
            names="Status", 
            hole=0.6,
            color="Status",
            color_manual={"Risky": "#FF3B30", "Safe": "#34C759"},
            template="plotly_dark"
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.8rem; margin-top:-20px;">COMPOSITION_ARRAY</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with vis_col2:
        st.markdown('<div class="bento-card" style="height: 400px;">', unsafe_allow_html=True)
        risky_text = " ".join([x['clause'] for x in processed_data if x['is_risky']])
        if risky_text:
            words = re.findall(r'\w+', risky_text.lower())
            stop_words = {'the', 'and', 'to', 'of', 'in', 'is', 'a', 'that', 'for', 'it', 'with', 'as', 'on'}
            keywords = [w for w in words if len(w) > 3 and w not in stop_words]
            keyword_counts = Counter(keywords).most_common(8)
            if keyword_counts:
                kw_df = pd.DataFrame(keyword_counts, columns=['Keyword', 'Frequency'])
                fig_bar = px.bar(
                    kw_df, 
                    x='Frequency', 
                    y='Keyword', 
                    orientation='h',
                    template="plotly_dark",
                    color_discrete_sequence=['#58A6FF']
                )
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=20, b=20, l=0, r=20),
                    xaxis_title=None,
                    yaxis_title=None,
                    height=300
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.write("Insufficient data for keyword analysis.")
        else:
            st.markdown('<div style="height:300px; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.2);">NO_RISK_DETECTED_FOR_ANALYSIS</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.8rem; margin-top:-20px;">TOP_RISK_FACTORS</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Detailed Clause Audit</span>', unsafe_allow_html=True)
    for i, item in enumerate(processed_data):
        risk_class = "risk-high" if item['is_risky'] else "risk-low"
        risk_text = "DANGER / HIGH RISK" if item['is_risky'] else "NOMINAL / LOW RISK"
        st.markdown(f"""
            <div class="glass-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <div style="display:flex; gap:10px; align-items:center;">
                        <span class="risk-tag {risk_class}">{risk_text}</span>
                    </div>
                    <span class="label-mono" style="opacity:0.5;">ID: C-{i+1:03} | CONF: {item['confidence']:.2%}</span>
                </div>
                <div style="font-size:1.1rem; color:#E1E4E8; line-height:1.6; margin-bottom: 20px;">
                    {item['clause']}
                </div>
        """, unsafe_allow_html=True)
        if item['is_risky']:
            if st.button(f"🔍 Perform Agentic Deep Audit", key=f"agent_{i}"):
                with st.spinner("Agentic Reasoning in Progress..."):
                    agent_res = analyze_risk_with_agent(item['clause'])
                    st.markdown(f"""
                        <div class="agentic-panel">
                            <div class="agent-title">
                                <span style="font-size: 1.2rem;">⚡</span> AGENTIC_INTELLIGENCE_REASONING_ENGINE
                            </div>
                            <div class="agent-text">
                                {agent_res['explanation']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="label-mono">Export Intelligence Report</span>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container" style="display: flex; gap: 20px;">', unsafe_allow_html=True)
    exp_col1, exp_col2, _ = st.columns([1, 1, 3])
    with exp_col1:
        json_report = generate_json_report(processed_data, metadata)
        st.download_button(
            label="📄 Download JSON",
            data=json_report,
            file_name=f"audit_report_{uploaded_file.name}.json",
            mime="application/json",
            use_container_width=True
        )
    with exp_col2:
        try:
            pdf_path = f"report_{uploaded_file.name}.pdf"
            generate_pdf_report(processed_data, metadata, pdf_path)
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            st.download_button(
                label="📑 Download PDF",
                data=pdf_bytes,
                file_name=f"audit_report_{uploaded_file.name}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            os.remove(pdf_path)
        except Exception as e:
            st.error(f"PDF Export failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
with col_right:
    if not uploaded_file:
        img_path = "/Users/gautamjha/MY-PROJECTS/FInal Projects/AI-ML-PROJECT-26/assets/Whisk_mwykjdnhjdnlfdz40iz2atotuwn4qtlxcdol1cm__1_-removebg-preview.png"
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <div style="text-align:center; width: 100%; display: flex; justify-content:center; align-items:center; padding: 20px;">
                    <img src="data:image/png;base64,{img_data}" class="pippo-float" 
                        style="max-width:850px; width: 100%; height: auto; filter: drop-shadow(0 0 30px rgba(255,255,255,0.1));">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:400px; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.05); border-radius:20px;">[ BRAND_ASSET_MISSING ]</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-container" style="background: rgba(88, 166, 255, 0.05); border-color: rgba(88, 166, 255, 0.2);">', unsafe_allow_html=True)
        st.markdown('<span class="label-mono">Live Audit Uplink</span>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
                <span class="label-mono" style="font-size: 0.55rem;">INTEGRITY_SCORE</span>
                <h1 style="color: #34C759; margin: 0; font-size: 3rem;">{int((len(processed_data)-risky_count)/len(processed_data)*100) if len(processed_data)>0 else 0}%</h1>
                <p style="color: rgba(255,255,255,0.4); font-size:0.7rem;">OPTIMIZED_LEGAL_DNA</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>" * 5, unsafe_allow_html=True)
st.markdown("""
<div style="border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 24px; display: flex; justify-content: space-between; align-items: center;">
    <span class="label-mono" style="font-weight: 900; color: #E91E63; letter-spacing: 2px;">PIPPO AI // GAUTAM BHARADWAJ SYSTEMS // 2026 EDITION</span>
    <span class="label-mono" style="opacity: 0.3; font-size: 0.6rem;">SYSTEM_NOMINAL // LATENCY_42MS // V2.0.1</span>
</div>
""", unsafe_allow_html=True)