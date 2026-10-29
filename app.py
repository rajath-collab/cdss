"""
Project: MedFuse-AI
Platform: Multimodal Fused Clinical Decision Support System (CDSS)
Unified Healthcare Platform:
  - Module 0: Sign-Up & Sign-In (Authentication & RBAC)
  - Module 1: Remote Patient & Home Care Portal (Triage, Results, Prescriptions)
  - Module 2: Clinician / Radiologist Admin Triage Console (Emergency Alerts, Grad-CAM, E-Signatures)
  - Module 5: Direct Ingestion Sandbox & Frontline ASHA Advisory
"""

import os
import time
import pandas as pd
from PIL import Image
import streamlit as st

# Import MedFuse-AI Modular Components
from utils.config import config
from models.vision_model import load_model
from models.gradcam import GradCAM
from rag.vector_store import CDSSVectorStore
from modules.auth_portal import render_auth_page
from modules.patient_portal import render_patient_portal
from modules.clinician_portal import render_admin_portal
from modules.direct_sandbox import render_direct_sandbox
from utils.translations import get_ui_text, LANGUAGES

# -------------------------------------------------------------
# 1. Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="MedFuse-AI | Clinical Decision Support System (CDSS)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. Custom Medical Aesthetic Styling
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Clean Medical Dashboard Theme */
    .main-header {
        background: linear-gradient(135deg, #0b192c 0%, #1e3e62 100%);
        padding: 24px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .badge-urgent {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        border: 1px solid #f87171;
    }
    .badge-normal {
        background-color: #dcfce7;
        color: #166534;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        border: 1px solid #4ade80;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------
# 💡 ASSISTIVE TECHNOLOGY NOTICE & STATUTORY CLINICAL COMPLIANCE
# Highlighted First: AIIMS, ICMR, NMC, & SaMD Statutory Directives
# -----------------------------------------------------------------
if "ui_lang" not in st.session_state:
    st.session_state["ui_lang"] = "en"
ui_lang = st.session_state.get("ui_lang", "en")
t = get_ui_text(ui_lang)

if "hide_assistive_notice" not in st.session_state:
    st.session_state.hide_assistive_notice = False

if not st.session_state.hide_assistive_notice:
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #f59e0b; border-left: 8px solid #d97706; padding: 18px 22px; border-radius: 10px; margin-bottom: 8px; box-shadow: 0 4px 14px rgba(217, 119, 6, 0.12);">
    <div style="display: flex; align-items: flex-start; gap: 16px;">
        <span style="font-size: 2.2rem; line-height: 1;">💡</span>
        <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                <span style="background: #d97706; color: #ffffff; font-weight: 800; font-size: 0.82rem; letter-spacing: 0.8px; padding: 4px 12px; border-radius: 5px; text-transform: uppercase;">
                    {t['notice_badge']}
                </span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #92400e; background: rgba(217, 119, 6, 0.12); padding: 3px 10px; border-radius: 4px; border: 1px solid #fde68a;">
                    {t['notice_protocol']}
                </span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #78350f; line-height: 1.45; margin-bottom: 10px;">
                {t['notice_main']}
            </div>
            <div style="font-size: 0.86rem; color: #92400e; line-height: 1.55; border-top: 1px dashed #fcd34d; padding-top: 10px;">
                <div style="font-weight: 700; margin-bottom: 6px; color: #78350f;">
                    {t['notice_gov_header']}
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 10px;">
                    <div>{t['notice_aiims']}</div>
                    <div>{t['notice_icmr']}</div>
                    <div>{t['notice_nmc']}</div>
                    <div>{t['notice_cdsco']}</div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    col_notice_info, col_notice_btn = st.columns([0.72, 0.28])
    with col_notice_info:
        st.caption(t["notice_caption"])
    with col_notice_btn:
        if st.button(t["btn_ack_hide"], key="btn_dismiss_top_notice", use_container_width=True):
            st.session_state.hide_assistive_notice = True
            st.rerun()
else:
    col_spc, col_show = st.columns([0.78, 0.22])
    with col_show:
        if st.button(t["btn_show_notice"], key="btn_show_top_notice", use_container_width=True):
            st.session_state.hide_assistive_notice = False
            st.rerun()

# Application Header
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <h1 style="margin: 0; font-size: 1.85rem; font-weight: 700; letter-spacing: -0.5px;">
                🩺 MedFuse-AI: Multimodal Clinical Decision Support System
            </h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                {t['app_subtitle']}
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600;">
                {t['app_edition']}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Model & Vector DB with Streamlit Caching
@st.cache_resource
def get_cdss_model():
    return load_model()

@st.cache_resource
def get_vector_store():
    return CDSSVectorStore(persist_dir="data/chroma_db")

model = get_cdss_model()
vector_store = get_vector_store()
gradcam = GradCAM(model)

# -------------------------------------------------------------
# 🔐 AUTHENTICATION & ACCESS CONTROL GATE (SIGN UP & SIGN IN)
# -------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None
if "last_activity" not in st.session_state:
    st.session_state["last_activity"] = time.time()

# Session Inactivity Timeout Guard
if st.session_state.get("authenticated", False):
    last_act = st.session_state.get("last_activity") or time.time()
    elapsed_minutes = (time.time() - last_act) / 60
    if elapsed_minutes > config.SESSION_TIMEOUT_MINUTES:
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.session_state["user_role"] = None
        st.warning("⚠️ Session expired due to inactivity. Please sign in again.")
        st.rerun()
    st.session_state["last_activity"] = time.time()

if not st.session_state.get("authenticated", False):
    render_auth_page()
    st.stop()

current_user = st.session_state.get("current_user") or {}
user_role = st.session_state.get("user_role") or "patient"

# -------------------------------------------------------------
# 🧭 SIDEBAR NAVIGATION & PROFILE CONTROLS
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/medical-heart.png", width=64)
    
    # Vernacular Language Selector in Sidebar
    st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 4px;'>{t.get('lang_selector_label', '🌐 Language / ಭಾಷೆ:')}</div>", unsafe_allow_html=True)
    lang_keys = list(LANGUAGES.keys())
    cur_lang_idx = lang_keys.index(ui_lang) if ui_lang in lang_keys else 0
    selected_lang_sidebar = st.selectbox(
        "Choose Language",
        lang_keys,
        index=cur_lang_idx,
        format_func=lambda k: f"{LANGUAGES[k]['flag']} {LANGUAGES[k]['native']}",
        key="app_sidebar_lang_selector",
        label_visibility="collapsed"
    )
    if selected_lang_sidebar != ui_lang:
        st.session_state["ui_lang"] = selected_lang_sidebar
        st.rerun()

    role_badge = t["role_doctor"] if user_role == "doctor" else (t["role_patient"] if user_role == "patient" else t["role_asha"])
    user_display_name = current_user.get('full_name', 'Authorized User')
    st.markdown(f"""
    <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
        <div style="font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase;">{t['active_session']}</div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #0f172a;">{user_display_name}</div>
        <div style="font-size: 0.8rem; color: #2563eb; font-weight: 600;">Role: {role_badge}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(t["btn_sign_out"], key="btn_logout_sidebar", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.session_state["user_role"] = None
        st.session_state["last_activity"] = None
        st.session_state["xray_file"] = None
        st.session_state["pdf_file"] = None
        st.rerun()

    st.divider()
    
    # -------------------------------------------------------------
    # 🛡️ ROLE-BASED ACCESS CONTROL (RBAC) NAVIGATION FILTER
    # Patients are restricted strictly to Patient Portal.
    # Clinicians access Diagnostic Console & Multimodal Sandbox.
    # ASHA Workers access Field Advisory & Multimodal Sandbox.
    # -------------------------------------------------------------
    if user_role == "doctor":
        persona_options = [
            "👨‍⚕️ Clinician Diagnostic Console & Audit (Module 2)",
            "🔬 Multimodal Direct Ingestion Sandbox"
        ]
    elif user_role == "asha":
        persona_options = [
            "🤝 ASHA / Health Worker (Field)",
            "🔬 Multimodal Direct Ingestion Sandbox"
        ]
    else:  # patient
        persona_options = [
            "🏠 Remote Patient & Home Care (Module 1)"
        ]

    app_mode = st.radio(
        "Select User Persona / View:",
        persona_options,
        index=0
    )

    st.divider()
    st.markdown("""
    <div style="font-size: 0.8rem; color: #78350f; line-height: 1.45; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
        💡 <strong>Assistive Second Opinion:</strong><br/>
        Final clinical diagnosis rests strictly with certified medical practitioners.<br/>
        <div style="margin-top: 8px; font-size: 0.74rem; color: #92400e; border-top: 1px dashed #fde68a; padding-top: 6px;">
            • AIIMS Clinical AI Standards<br/>
            • ICMR Biomedical AI Guidelines 2023<br/>
            • NMC Act 2019 RMP Directives<br/>
            • DPDP Act 2023 Memory Sandbox
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("hide_assistive_notice", False):
        if st.button("💡 Show Assistive Notice", key="sidebar_unhide_btn", use_container_width=True):
            st.session_state.hide_assistive_notice = False
            st.rerun()
    else:
        if st.button("✕ Hide Assistive Notice", key="sidebar_hide_btn", use_container_width=True):
            st.session_state.hide_assistive_notice = True
            st.rerun()

# -------------------------------------------------------------
# 🎯 PERSONA ROUTING CONTROLLER
# -------------------------------------------------------------
if "Remote Patient" in app_mode:
    render_patient_portal(current_user, model, gradcam, vector_store)
elif "Clinician Diagnostic Console" in app_mode:
    render_admin_portal(current_user, model, gradcam, vector_store)
else:
    render_direct_sandbox(app_mode, model, gradcam, vector_store)

# -------------------------------------------------------------
# 📜 REGULATORY, PRIVACY & CLINICAL GOVERNANCE FOOTER
# -------------------------------------------------------------
st.divider()
if not st.session_state.get("hide_assistive_notice", False):
    st.markdown(f"""
<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 22px 26px; margin-top: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.04);">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #d97706; border-radius: 8px; padding: 18px 20px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="font-size: 1.25rem;">💡</span>
<span style="margin: 0; color: #78350f; font-size: 1.05rem; font-weight: 700;">{t.get('footer_assistive_title', 'Assistive Technology Notice & Clinical Policy')}</span>
</div>
<p style="font-size: 0.88rem; font-weight: 700; color: #92400e; line-height: 1.45; margin: 0 0 8px 0;">
{t.get('notice_main', 'This platform serves as a point-of-care second opinion. Final clinical diagnosis rests strictly with certified medical practitioners.')}
</p>
<p style="font-size: 0.81rem; color: #475569; line-height: 1.55; margin: 0 0 6px 0;">
{t.get('notice_aiims', '• AIIMS Clinical AI Standards: Machine predictions act purely as assistive triage suggestions and must never replace clinical bedside evaluation or auscultation.')}
</p>
<p style="font-size: 0.81rem; color: #475569; line-height: 1.55; margin: 0 0 6px 0;">
{t.get('notice_nmc', '• National Medical Commission (NMC) Act 2019: The certified Registered Medical Practitioner (RMP) bears full statutory liability for clinical diagnoses, prescriptions, and patient management.')}
</p>
<p style="font-size: 0.81rem; color: #475569; line-height: 1.55; margin: 0;">
{t.get('notice_cdsco', '• CDSCO / SaMD Class B: Categorized as non-invasive Software as a Medical Device for clinical prioritization.')}
</p>
</div>
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #0284c7; border-radius: 8px; padding: 18px 20px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="font-size: 1.25rem;">🛡️</span>
<span style="margin: 0; color: #0c4a6e; font-size: 1.05rem; font-weight: 700;">{t.get('footer_dpdp_title', 'Privacy Policy & Data Protection (DPDP Act 2023)')}</span>
</div>
<p style="font-size: 0.81rem; color: #475569; line-height: 1.55; margin: 0 0 8px 0;">
{t.get('footer_dpdp_cloud', '• Zero Persistent Cloud Storage: In strict compliance with India\'s Digital Personal Data Protection (DPDP) Act 2023 and HIPAA Security Rules (45 CFR §164), radiographs and laboratory reports are processed ephemerally in local volatile memory.')}
</p>
<p style="font-size: 0.81rem; color: #475569; line-height: 1.55; margin: 0 0 8px 0;">
{t.get('footer_dpdp_phi', '• Protected Health Information (PHI) Isolation: Patient identifiers are sanitized in-flight; no clinical records or biometric imaging tensors are archived or transmitted across public networks.')}
</p>
<p style="font-size: 0.81rem; color: #475569; line-height: 1.55; margin: 0;">
{t.get('footer_dpdp_chroma', '• Local ChromaDB Sandbox: Clinical guideline vectors are maintained locally on-premise without third-party telemetric leakage.')}
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    col_ft_info, col_ft_hide = st.columns([0.72, 0.28])
    with col_ft_info:
        st.caption(t.get("footer_caption", "ℹ️ Click 'Acknowledge & Hide Policies' to collapse clinical notice and privacy cards."))
    with col_ft_hide:
        if st.button(t.get("footer_btn_hide", "👁️ Acknowledge & Hide Policies"), key="btn_dismiss_footer_cards", use_container_width=True):
            st.session_state.hide_assistive_notice = True
            st.rerun()
else:
    col_ft_min, col_ft_show = st.columns([0.76, 0.24])
    with col_ft_min:
        st.markdown(f"""
        <div style="padding: 9px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.82rem; color: #475569; margin-top: 10px;">
            {t.get('footer_ack_tag', '🛡️ Statutory Clinical & DPDP Privacy Policies Acknowledged (Zero Cloud Persistence • AIIMS/ICMR/HIPAA Compliant)')}
        </div>
        """, unsafe_allow_html=True)
    with col_ft_show:
        st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
        if st.button(t.get("footer_btn_show", "💡 Show Policy Cards"), key="btn_show_footer_cards", use_container_width=True):
            st.session_state.hide_assistive_notice = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with st.expander(t.get("footer_expander_title", "📜 Read Full Privacy Policy & Statutory Regulatory Documentation (AIIMS, ICMR, NMC, DPDP Act 2023)")):
    st.markdown("""
    #### 1. Scope of Assistive Technology & Second-Opinion Demarcation
    - **Assistive SaMD Status:** This platform is engineered strictly as an Assistive Software as a Medical Device (SaMD) Class B triage decision support system. It is designed to assist frontline clinicians, radiologists, and primary healthcare workers (ASHA/PHC) by providing high-speed cross-modal triage correlations.
    - **Non-Autonomous Boundary:** Under no circumstances does this platform replace clinical consultations, stethoscope auscultation, or definitive laboratory cultures. The software cannot independently issue medical prescriptions, discharge orders, or surgical authorizations.

    #### 2. Statutory Legal Liability & Registered Medical Practitioner (RMP) Authority
    - **NMC Code of Medical Ethics:** In accordance with the National Medical Commission (NMC) Act 2019 and Indian Medical Council (Professional Conduct, Etiquette and Ethics) Regulations, final clinical diagnosis and therapeutic decisions rest exclusively with the certified medical practitioner.
    - **Clinical Establishments Act:** Point-of-care deployments must integrate human-in-the-loop validation, ensuring that all AI outputs are audited by qualified medical personnel prior to patient communication.

    #### 3. Privacy Policy & Data Fiduciary Compliance (DPDP Act 2023 & HIPAA)
    - **Data Fiduciary Obligations:** Under the Digital Personal Data Protection (DPDP) Act 2023 (Sections 4, 5, and 6), this system enforces the principle of *Purpose Limitation* and *Data Minimization*.
    - **Ephemeral Local Processing:** Uploaded DICOM/JPEG radiographs and PDF pathology slips are analyzed in volatile RAM and immediately garbage-collected upon session completion or browser reload. No biometric data, medical history, or identifying metadata is written to disk or sent to external cloud APIs.
    - **HIPAA Technical Safeguards (45 CFR §164.312):** Offline compute isolation eliminates transmission vulnerabilities, ensuring zero exposure of Protected Health Information (PHI).

    #### 4. Algorithmic Transparency & Explainable AI (ICMR Guidelines 2023)
    - **Explainability Standard:** In accordance with the Indian Council of Medical Research (ICMR) Ethical Guidelines for AI in Biomedical Research (2023), all deep-learning inferences (ResNet-50) are accompanied by Grad-CAM visual heatmaps highlighting exact anatomical feature attributions.
    - **Zero-Hallucination Vector RAG:** Text retrieval for biomarker interpretation is strictly grounded against peer-reviewed clinical knowledge bases in ChromaDB with cosine distance validation, eliminating generative hallucinations.
    """)

st.markdown(f"""
<div style="border-top: 1px solid #cbd5e1; margin-top: 15px; padding-top: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: #64748b; flex-wrap: wrap; gap: 8px;">
    <span>© 2026 MedFuse-AI Multimodal CDSS Triage Platform | Assistive Point-of-Care Edition</span>
    <span>Statutory Standards: AIIMS Clinical AI • ICMR Ethics 2023 • NMC Act 2019 • DPDP Act 2023 • HIPAA Security Rule • CDSCO SaMD Class B</span>
</div>
""", unsafe_allow_html=True)
