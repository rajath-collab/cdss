"""
Module 1: Remote Patient & Home Care View
Lead: Student 1 (System Architect)
"""
import streamlit as st
import time

def render_patient_portal():
    st.markdown("""
        <div class="med-card">
            <h2 style="margin: 0; color: #38BDF8;">🏠 Remote Point-of-Care Home Portal</h2>
            <p style="color: #94A3B8; margin: 4px 0 0 0;">Upload your chest radiograph or lab test slip from home for instant AI triage.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📸 1. Chest Radiograph")
        uploaded_xray = st.file_uploader("Snap or upload X-ray photo", type=["png", "jpg", "jpeg"], key="p_xray")
        if uploaded_xray:
            st.image(uploaded_xray, caption="Uploaded Radiograph", width=300)

    with col2:
        st.markdown("### 📋 2. Pathology Lab Slip")
        uploaded_lab = st.file_uploader("Upload Blood/CBC report (PDF/Image)", type=["pdf", "png", "jpg"], key="p_lab")
        fever = st.slider("Fever duration (Days):", 0, 14, 2)
        spo2 = st.number_input("SpO2 Blood Oxygen (%):", min_value=70, max_value=100, value=96)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🔍 Run Remote Health Triage", use_container_width=True):
        with st.spinner("Fusing Thoracic Vision and Pathology Lab Findings..."):
            time.sleep(1.2)

        if spo2 < 92:
            st.markdown('<span class="triage-badge-red">🔴 CRITICAL TRIAGE: Low Oxygen & Severe Consolidation</span>', unsafe_allow_html=True)
            st.error("Urgent Medical Attention Advised: An emergency tele-consultation has been triggered.")
        else:
            st.markdown('<span class="triage-badge-amber">🟡 MODERATE RISK: Focal Infiltration Detected</span>', unsafe_allow_html=True)
            st.warning("Visit your nearest Primary Health Centre (PHC) within 24 hours. Voice advisory sent.")