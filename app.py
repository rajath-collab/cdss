"""
Project: MedFuse-AI
Platform: Multimodal Clinical Decision Support System (CDSS)
Point-of-Care Triage, Radiography Grad-CAM & Tele-ICU Platform
Complete Frontend UI Implementation:
  - Module 0: Authentication & Role-Based Access Control (RBAC)
  - Module 1: Remote Patient & Home Care Portal
  - Module 2: Clinician / Radiologist Admin Triage Console
  - Module 4: Interactive RAG Lab Assistant & Clinical Knowledge Window
  - Module 5: Direct Multimodal Ingestion Sandbox & Frontline ASHA Advisory
"""
import streamlit as st
import time
from src.config import init_session_state, DOCTOR_DATABASE, LANGUAGES
from src.ui.styles import CUSTOM_CSS
from src.ui.auth_view import render_auth_page
from src.ui.patient_view import render_patient_portal
from src.ui.admin_view import render_admin_portal
from src.ui.sandbox_view import render_direct_sandbox
from src.ui.rag_view import render_rag_window
from src.ui.translations import get_ui_text

# -------------------------------------------------------------
# 1. Page Configuration & Theme
# -------------------------------------------------------------
st.set_page_config(
    page_title="MedFuse-AI | Clinical Decision Support System (CDSS)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_session_state()

ui_lang = st.session_state.get("ui_lang", "en")
t = get_ui_text(ui_lang)

# -----------------------------------------------------------------
# 💡 ASSISTIVE TECHNOLOGY NOTICE & STATUTORY CLINICAL COMPLIANCE
# AIIMS, ICMR, NMC, & SaMD Statutory Directives
# -----------------------------------------------------------------
if not st.session_state.get("hide_assistive_notice", False):
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #f59e0b; border-left: 8px solid #d97706; padding: 18px 22px; border-radius: 10px; margin-bottom: 12px; box-shadow: 0 4px 14px rgba(217, 119, 6, 0.12);">
    <div style="display: flex; align-items: flex-start; gap: 16px;">
        <span style="font-size: 2.2rem; line-height: 1;">💡</span>
        <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                <span style="background: #d97706; color: #ffffff; font-weight: 800; font-size: 0.82rem; letter-spacing: 0.8px; padding: 4px 12px; border-radius: 5px; text-transform: uppercase;">
                    {t.get('notice_badge', 'STATUTORY DIRECTIVE')}
                </span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #92400e; background: rgba(217, 119, 6, 0.12); padding: 3px 10px; border-radius: 4px; border: 1px solid #fde68a;">
                    {t.get('notice_protocol', 'AIIMS / ICMR / NMC PROTOCOL')}
                </span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #78350f; line-height: 1.45; margin-bottom: 8px;">
                {t.get('notice_main', 'Assistive Second Opinion: Final clinical diagnosis rests strictly with certified medical practitioners.')}
            </div>
            <div style="font-size: 0.84rem; color: #92400e; line-height: 1.5; border-top: 1px dashed #fcd34d; padding-top: 8px;">
                <div>{t.get('notice_aiims', '• AIIMS Clinical AI Standards: Machine predictions act purely as assistive triage suggestions.')}</div>
                <div>{t.get('notice_nmc', '• NMC Act 2019: Registered Medical Practitioner (RMP) holds exclusive legal liability for clinical diagnoses.')}</div>
                <div>{t.get('notice_cdsco', '• SaMD Class B / DPDP Act 2023: Non-invasive triage decision support with client-side memory isolation.')}</div>
            </div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    col_n_info, col_n_btn = st.columns([0.75, 0.25])
    with col_n_info:
        st.caption(t.get("notice_caption", "ℹ️ Click 'Acknowledge & Hide Notice' to minimize this compliance banner."))
    with col_n_btn:
        if st.button(t.get("btn_ack_hide", "👁️ Acknowledge & Hide Notice"), key="btn_dismiss_notice", use_container_width=True):
            st.session_state.hide_assistive_notice = True
            st.rerun()
else:
    col_s1, col_s2 = st.columns([0.8, 0.2])
    with col_s2:
        if st.button(t.get("btn_show_notice", "💡 Show Assistive Notice"), key="btn_show_notice", use_container_width=True):
            st.session_state.hide_assistive_notice = False
            st.rerun()

# -------------------------------------------------------------
# 2. Authentication Gateway Gate & Session Security Guard
# -------------------------------------------------------------
# Session Inactivity Timeout Guard (HIPAA & DPDP Act Compliance)
if st.session_state.get("authenticated", False):
    last_act = st.session_state.get("last_activity") or time.time()
    elapsed_minutes = (time.time() - last_act) / 60
    if elapsed_minutes > 60:
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.session_state["user_role"] = None
        st.warning("⚠️ Clinical session expired due to inactivity. Please sign in again.")
        st.rerun()
    st.session_state["last_activity"] = time.time()

if not st.session_state["authenticated"]:
    render_auth_page()
    st.stop()

# -------------------------------------------------------------
# 3. Authenticated Router & Sidebar Navigation
# -------------------------------------------------------------
user_role = st.session_state.get("user_role", "doctor")
user_id = st.session_state.get("user_id", "Authorized User")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/medical-heart.png", width=64)
    
    # Vernacular Language Selector
    st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 4px;'>{t.get('lang_selector_label', '🌐 Language / ಭಾಷೆ:')}</div>", unsafe_allow_html=True)
    lang_keys = list(LANGUAGES.keys())
    cur_idx = lang_keys.index(ui_lang) if ui_lang in lang_keys else 0
    sel_lang = st.selectbox(
        "Choose Language",
        lang_keys,
        index=cur_idx,
        format_func=lambda k: f"{LANGUAGES[k]['flag']} {LANGUAGES[k]['native']}",
        key="sidebar_lang_selector",
        label_visibility="collapsed"
    )
    if sel_lang != ui_lang:
        st.session_state["ui_lang"] = sel_lang
        st.rerun()

    role_badge = t.get("role_doctor", "Clinician MD") if user_role == "doctor" else (t.get("role_asha", "ASHA Lead") if user_role == "asha" else t.get("role_patient", "Remote Patient"))
    st.markdown(f"""
    <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
        <div style="font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase;">{t.get('active_session', 'ACTIVE CLINICAL SESSION')}</div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #0f172a;">{user_id}</div>
        <div style="font-size: 0.8rem; color: #0284c7; font-weight: 600;">Role: {role_badge}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t.get("btn_sign_out", "🚪 Sign Out"), key="btn_logout_side", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user_role"] = None
        st.rerun()

    st.divider()

    # RBAC Persona Navigation Filter
    if user_role == "doctor":
        nav_options = [
            "👨‍⚕️ Clinician Diagnostic Console & Audit (Module 2)",
            "🔬 Multimodal Direct Ingestion Sandbox (Module 5)",
            "💬 Clinical Knowledge & RAG Assistant (Module 4)"
        ]
    elif user_role == "asha":
        nav_options = [
            "🤝 ASHA / Frontline Health Worker (Field Mode)",
            "🔬 Multimodal Direct Ingestion Sandbox (Module 5)",
            "💬 Clinical Knowledge & RAG Assistant (Module 4)"
        ]
    else:  # patient
        nav_options = [
            "🏠 Remote Patient & Home Care (Module 1)",
            "💬 Clinical Knowledge & RAG Assistant (Module 4)"
        ]

    app_mode = st.radio(
        "Select User Persona / Component View:",
        nav_options,
        index=0
    )

    st.divider()
    st.markdown("""
    <div style="font-size: 0.8rem; color: #78350f; line-height: 1.45; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
        💡 <strong>Point-of-Care Advisory:</strong><br/>
        All AI inferences act as assistive recommendations under human-in-the-loop oversight.
        <div style="margin-top: 8px; font-size: 0.74rem; color: #92400e; border-top: 1px dashed #fde68a; padding-top: 6px;">
            • AIIMS Clinical AI Standards<br/>
            • ICMR Biomedical AI Ethics 2023<br/>
            • NMC Act 2019 RMP Directives
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 🎯 COMPONENT ROUTING CONTROLLER
# -------------------------------------------------------------
if "Remote Patient" in app_mode:
    render_patient_portal()
elif "Clinician Diagnostic Console" in app_mode:
    render_admin_portal()
elif "Knowledge & RAG" in app_mode:
    render_rag_window(user_persona=user_role)
elif "ASHA" in app_mode:
    render_direct_sandbox(app_mode="ASHA Field Mode")
else:
    render_direct_sandbox(app_mode="Multimodal Sandbox")

# -------------------------------------------------------------
# 📜 REGULATORY, PRIVACY & CLINICAL GOVERNANCE FOOTER
# -------------------------------------------------------------
st.divider()
st.markdown("""
<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px 24px; margin-top: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.04);">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px;">
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #d97706; border-radius: 8px; padding: 16px;">
            <div style="font-weight: 700; color: #78350f; font-size: 0.98rem; margin-bottom: 6px;">
                💡 Assistive SaMD Class B Clinical Policy
            </div>
            <p style="font-size: 0.81rem; color: #475569; line-height: 1.5; margin: 0;">
                Engineered as a point-of-care second-opinion aid. Under the National Medical Commission (NMC) Act 2019, diagnostic and therapeutic authority rests exclusively with certified medical doctors.
            </p>
        </div>
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #0284c7; border-radius: 8px; padding: 16px;">
            <div style="font-weight: 700; color: #0c4a6e; font-size: 0.98rem; margin-bottom: 6px;">
                🛡️ DPDP Act 2023 & HIPAA Security Safeguards
            </div>
            <p style="font-size: 0.81rem; color: #475569; line-height: 1.5; margin: 0;">
                Strict client-side volatile memory processing. Zero cloud telemetric leakage. Protected Health Information (PHI) is isolated in compliance with Indian healthcare IT regulations.
            </p>
        </div>
    </div>
    <div style="border-top: 1px solid #e2e8f0; margin-top: 14px; padding-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: #64748b; flex-wrap: wrap; gap: 8px;">
        <span>© 2026 MedFuse-AI Multimodal Clinical Decision Support System | Point-of-Care Edition</span>
        <span>AIIMS Standards • ICMR Ethics 2023 • NMC Act 2019 • DPDP Act 2023 • CDSCO SaMD Class B</span>
    </div>
</div>
""", unsafe_allow_html=True)
