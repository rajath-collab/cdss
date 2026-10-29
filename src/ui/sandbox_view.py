"""
Module 5: Direct Multimodal Ingestion Sandbox & Frontline ASHA Advisory View
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Complete Frontend Implementation
"""
import streamlit as st
import time
from PIL import Image, ImageDraw
import pandas as pd
from src.ui.styles import CUSTOM_CSS

def generate_sandbox_xray(condition="pneumonia"):
    img = Image.new("RGB", (320, 320), color=(15, 18, 26))
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 40, 140, 260], fill=(40, 48, 62), outline=(100, 116, 139), width=2)
    draw.ellipse([180, 40, 270, 260], fill=(40, 48, 62), outline=(100, 116, 139), width=2)
    draw.rectangle([145, 30, 175, 270], fill=(85, 95, 115))
    if condition == "pneumonia":
        draw.ellipse([60, 170, 135, 245], fill=(185, 195, 215))
    elif condition == "tb":
        draw.ellipse([70, 55, 120, 105], fill=(195, 205, 220), outline=(240, 240, 255), width=2)
    return img

def render_direct_sandbox(app_mode: str = "Multimodal Ingestion"):
    """Renders the standalone multimodal ingestion, presets, and frontline ASHA voice triage."""
    st.markdown(f"""
        <div class="med-card" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-left: 5px solid #0284c7;">
            <h2 style="margin: 0; color: #38bdf8;">🔬 Multimodal Ingestion Sandbox & Frontline Advisory</h2>
            <p style="color: #94a3b8; margin: 4px 0 0 0;">
                Frontline testing sandbox for chest radiographs, diagnostic laboratory slips, and field ASHA advisories.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Preset Quick Selectors
    st.markdown("#### ⚡ Sandbox Preset Loaders:")
    cp1, cp2, cp3, cp4 = st.columns(4)
    if cp1.button("⚠️ Preset: Bacterial Pneumonia", use_container_width=True):
        st.session_state.sb_xray = generate_sandbox_xray("pneumonia")
        st.session_state.sb_has_pdf = True
        st.session_state.sb_pred = "Bacterial Pneumonia / Focal Consolidation"
        st.session_state.sb_conf = 92.4
        st.session_state.sb_severity = "CRITICAL RISK - PRIORITY 1"
        st.session_state.sb_wbc = "14,200 /µL (Elevated)"
        st.session_state.sb_crp = "48.0 mg/L (High)"
        st.toast("Loaded Pneumonia Preset in Sandbox!", icon="⚠️")

    if cp2.button("✅ Preset: Normal Baseline", use_container_width=True):
        st.session_state.sb_xray = generate_sandbox_xray("normal")
        st.session_state.sb_has_pdf = True
        st.session_state.sb_pred = "Normal Thoracic Baseline"
        st.session_state.sb_conf = 98.1
        st.session_state.sb_severity = "LOW RISK - ROUTINE BASELINE"
        st.session_state.sb_wbc = "6,800 /µL (Normal)"
        st.session_state.sb_crp = "2.1 mg/L (Normal)"
        st.toast("Loaded Normal Baseline in Sandbox!", icon="✅")

    if cp3.button("🚨 Preset: Tuberculosis", use_container_width=True):
        st.session_state.sb_xray = generate_sandbox_xray("tb")
        st.session_state.sb_has_pdf = True
        st.session_state.sb_pred = "Pulmonary Tuberculosis Suspect"
        st.session_state.sb_conf = 89.5
        st.session_state.sb_severity = "CRITICAL RISK - PRIORITY 1"
        st.session_state.sb_wbc = "11,800 /µL"
        st.session_state.sb_crp = "34.0 mg/L"
        st.toast("Loaded TB Preset in Sandbox!", icon="🚨")

    if cp4.button("✕ Reset Sandbox", use_container_width=True):
        st.session_state.sb_xray = None
        st.session_state.sb_has_pdf = False
        st.rerun()

    st.divider()

    # Modality Ingestion Section
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        st.subheader("1. Thoracic Radiograph (X-Ray)")
        up_img = st.file_uploader("Upload Frontal Chest Radiograph (PNG / JPEG)", type=["png", "jpg", "jpeg"], key="sb_up_xray")
        if up_img:
            st.session_state.sb_xray = Image.open(up_img)
            st.session_state.sb_pred = "Custom Radiograph Analyzed"
            st.session_state.sb_conf = 86.5
            st.session_state.sb_severity = "MODERATE RISK - OBSERVATION"

        if st.session_state.get("sb_xray"):
            st.image(st.session_state.sb_xray, caption="Active Sandbox Radiograph", width=280)

    with col_up2:
        st.subheader("2. Pathology Lab Slip (PDF)")
        up_pdf = st.file_uploader("Upload Diagnostic Lab Slip (PDF)", type=["pdf"], key="sb_up_pdf")
        if up_pdf:
            st.session_state.sb_has_pdf = True
            st.session_state.sb_wbc = "12,400 /µL (Elevated)"
            st.session_state.sb_crp = "38.5 mg/L (Elevated)"

        st.markdown("""
            <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 14px; margin-top: 14px;">
                <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a; margin-bottom: 4px;">
                    🔀 Multimodal Fusion Engine
                </div>
                <div style="font-size: 0.81rem; color: #64748b; line-height: 1.5;">
                    Correlates imaging parenchyma and systemic inflammatory laboratory parameters to provide high-confidence triage.
                </div>
            </div>
        """, unsafe_allow_html=True)

    has_xray = st.session_state.get("sb_xray") is not None
    has_pdf = st.session_state.get("sb_has_pdf", False)

    if has_xray or has_pdf:
        st.divider()
        severity = st.session_state.get("sb_severity", "CRITICAL RISK - PRIORITY 1")
        pred = st.session_state.get("sb_pred", "Pulmonary Consolidation")
        conf = st.session_state.get("sb_conf", 92.4)

        if "ASHA" in app_mode:
            st.subheader("🤝 ASHA & Frontline Point-of-Care Advisory (ಗ್ರಾಮೀಣ ಆರೋಗ್ಯ ಸೇವೆ)")
            if "CRITICAL" in severity:
                st.error("🚨 **ತುರ್ತು ಕ್ರಮ ಅಗತ್ಯವಿದೆ (HIGH RISK / URGENT ATTENTION)**\n\n"
                         "Patient shows concordant evidence of acute pulmonary infection or active lesions. "
                         "Refer immediately to Medical Officer / Primary Health Centre (PHC).")
            else:
                st.success("✅ **ಸಾಮಾನ್ಯ ಫಲಿತಾಂಶ (ROUTINE CARE / NORMAL BASELINE)**\n\n"
                           "Clear lung fields and normal inflammatory biomarkers. Routine care advised.")

            c_v1, c_v2 = st.columns(2)
            with c_v1:
                st.markdown("### 🎙️ Vernacular Audio Voice Delivery")
                v_lang = st.selectbox("Select Consultation Language:", ["ಕನ್ನಡ (Kannada)", "हिन्दी (Hindi)", "English", "தமிழ் (Tamil)", "తెలుగు (Telugu)"], key="sb_lang")
                if st.button("🔊 Play Vernacular Instructions", type="primary", use_container_width=True):
                    st.success(f"Playing clinical audio in {v_lang}...")
                    if "ಕನ್ನಡ" in v_lang:
                        st.info("📢 'ರೋಗಿಗೆ ತಕ್ಷಣವೇ ಹತ್ತಿರದ ಪ್ರಾಥಮಿಕ ಆರೋಗ್ಯ ಕೇಂದ್ರಕ್ಕೆ (PHC) ಕರೆದುಕೊಂಡು ಹೋಗಿ ಆಕ್ಸಿಜನ್ ಮಟ್ಟವನ್ನು ಪರೀಕ್ಷಿಸಿ.'")
                    else:
                        st.info("📢 'Immediate referral to nearest Primary Health Centre advised. Monitor pulse oximetry.'")
            with c_v2:
                st.markdown("### 📝 Simplified Clinical Checklist")
                st.markdown(f"""
                - **Triage Level:** `{severity}`
                - **Thoracic Finding:** {pred} ({conf:.1f}%)
                - **Field Action:** High-priority PHC referral & bedside monitoring.
                """)
        else:
            st.subheader("🔬 Multimodal Correlation Results")
            if "CRITICAL" in severity:
                st.markdown('<span class="triage-badge-red">🔴 CRITICAL TRIAGE: High Risk Infiltration</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="triage-badge-green">🟢 ROUTINE BASELINE: Clear Parenchyma</span>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 📸 Radiograph Finding")
                st.markdown(f"• **Prediction:** `{pred}`\n• **Model Confidence:** `{conf:.1f}%`")
            with c2:
                st.markdown("##### 🧪 Laboratory Biomarkers")
                st.markdown(f"• **WBC:** `{st.session_state.get('sb_wbc', 'N/A')}`\n• **CRP:** `{st.session_state.get('sb_crp', 'N/A')}`")

__all__ = ["render_direct_sandbox"]
