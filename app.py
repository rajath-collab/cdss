"""
Project: MedFuse-AI
Platform: Multimodal Clinical Decision Support System (CDSS)
Point-of-Care Triage, Radiography Grad-CAM & Tele-ICU Platform
"""
import streamlit as st
import time
from src.config import init_session_state, DOCTOR_DATABASE, LANGUAGES
from src.ui.styles import CUSTOM_CSS
from src.ui.patient_view import render_patient_portal
from src.ui.admin_view import render_admin_portal

# -------------------------------------------------------------
# 1. Page Configuration & Aesthetic Theme
# -------------------------------------------------------------
st.set_page_config(page_title="MedFuse-AI | CDSS", page_icon="🩺", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_session_state()

# -------------------------------------------------------------
# 💡 ASSISTIVE TECHNOLOGY NOTICE & STATUTORY CLINICAL COMPLIANCE
# AIIMS, ICMR, NMC, & SaMD Statutory Directives
# -------------------------------------------------------------
if not st.session_state.get("hide_assistive_notice", False):
    st.markdown("""
<div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #f59e0b; border-left: 8px solid #d97706; padding: 18px 22px; border-radius: 10px; margin-bottom: 12px; box-shadow: 0 4px 14px rgba(217, 119, 6, 0.12);">
    <div style="display: flex; align-items: flex-start; gap: 16px;">
        <span style="font-size: 2.2rem; line-height: 1;">💡</span>
        <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                <span style="background: #d97706; color: #ffffff; font-weight: 800; font-size: 0.82rem; letter-spacing: 0.8px; padding: 4px 12px; border-radius: 5px; text-transform: uppercase;">
                    STATUTORY DIRECTIVE
                </span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #92400e; background: rgba(217, 119, 6, 0.12); padding: 3px 10px; border-radius: 4px; border: 1px solid #fde68a;">
                    AIIMS / ICMR / NMC PROTOCOL
                </span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #78350f; line-height: 1.45; margin-bottom: 8px;">
                Assistive Second Opinion: Final clinical diagnosis rests strictly with certified medical practitioners.
            </div>
            <div style="font-size: 0.84rem; color: #92400e; line-height: 1.5; border-top: 1px dashed #fcd34d; padding-top: 8px;">
                • AIIMS Clinical AI Standards: Machine predictions act purely as assistive triage suggestions and must never replace clinical bedside evaluation.<br/>
                • NMC Act 2019: Registered Medical Practitioner (RMP) holds exclusive legal liability for all medical diagnoses and therapeutic prescriptions.<br/>
                • DPDP Act 2023 & HIPAA: Ephemeral zero persistent cloud storage ensures local client data isolation.
            </div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    col_n_info, col_n_btn = st.columns([0.75, 0.25])
    with col_n_info:
        st.caption("ℹ️ Click 'Acknowledge & Hide Notice' to minimize this compliance banner during demonstration.")
    with col_n_btn:
        if st.button("👁️ Acknowledge & Hide Notice", key="btn_dismiss_notice", use_container_width=True):
            st.session_state.hide_assistive_notice = True
            st.rerun()
else:
    col_s1, col_s2 = st.columns([0.8, 0.2])
    with col_s2:
        if st.button("💡 Show Assistive Notice", key="btn_show_notice", use_container_width=True):
            st.session_state.hide_assistive_notice = False
            st.rerun()

# -------------------------------------------------------------
# 2. Authentication Gateway
# -------------------------------------------------------------
if not st.session_state["authenticated"]:
    st.markdown("""
        <div style="text-align: center; margin: 25px 0 20px 0;">
            <div style="font-size: 3.2rem;">🩺</div>
            <h1 style="color: #0284c7; margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.5px;">
                MEDFUSE-AI POINT-OF-CARE
            </h1>
            <p style="color: #64748b; margin-top: 5px; font-size: 1rem;">
                Multimodal Fused Clinical Decision Support & Tele-ICU Platform
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 2, 1])

    with col_center:
        tab_patient, tab_doctor = st.tabs(["👤 Patient / Home User", "👨‍⚕️ Clinician / Radiologist (Admin)"])

        with tab_patient:
            st.markdown("##### Remote Patient Home Care Sign In")
            phone = st.text_input("Mobile Number:", value="9845012345", placeholder="Enter 10-digit number")
            otp = st.text_input("OTP (Demo: 123456):", value="123456", type="password")
            
            if st.button("🚀 Sign In as Patient", type="primary", use_container_width=True):
                if otp == "123456":
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "patient"
                    st.session_state["user_id"] = f"+91 {phone}" if phone else "Patient"
                    st.rerun()
                else:
                    st.error("Invalid OTP. Use demo OTP: 123456")

            st.divider()
            st.markdown("<p style='font-size: 0.82rem; font-weight: 600; color: #475569;'>⚡ Quick Viva Demo Access:</p>", unsafe_allow_html=True)
            if st.button("🏠 Instant Demo: Rajesh Kumar (Patient)", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "patient"
                st.session_state["user_id"] = "+91 9845012345 (Rajesh Kumar)"
                st.rerun()

        with tab_doctor:
            st.markdown("##### Clinician Diagnostic Console Authorization")
            doc_reg = st.selectbox("Medical Council Reg No:", list(DOCTOR_DATABASE.keys()))
            doc_pin = st.text_input("Doctor Security PIN (Demo: 7788):", value="7788", type="password")
            
            if st.button("🔒 Authorize Clinician Console", type="primary", use_container_width=True):
                if doc_pin == DOCTOR_DATABASE[doc_reg]["pin"]:
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "doctor"
                    st.session_state["user_id"] = f"{DOCTOR_DATABASE[doc_reg]['name']} ({doc_reg})"
                    st.rerun()
                else:
                    st.error("Invalid Doctor PIN. Enter 7788.")

            st.divider()
            st.markdown("<p style='font-size: 0.82rem; font-weight: 600; color: #475569;'>⚡ Quick Viva Demo Access:</p>", unsafe_allow_html=True)
            if st.button("👨‍⚕️ Instant Demo: Dr. Ramesh Rao (Doctor)", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "doctor"
                st.session_state["user_id"] = "Dr. Ramesh Rao, MD (KMC-58291)"
                st.rerun()

# -------------------------------------------------------------
# 3. Authenticated Router
# -------------------------------------------------------------
else:
    # Top User Navigation Bar
    c1, c2, c3 = st.columns([4, 1.2, 0.8])
    with c1:
        st.markdown(f"**Logged in as:** `{st.session_state['user_id']}` &nbsp;|&nbsp; Role: `<span class='triage-badge-green'>{st.session_state['user_role'].upper()}</span>`", unsafe_allow_html=True)
    with c2:
        lang_keys = list(LANGUAGES.keys())
        cur_lang = st.session_state.get("ui_lang", "en")
        cur_idx = lang_keys.index(cur_lang) if cur_lang in lang_keys else 0
        sel_lang = st.selectbox(
            "Language",
            lang_keys,
            index=cur_idx,
            format_func=lambda k: f"{LANGUAGES[k]['flag']} {LANGUAGES[k]['native']}",
            label_visibility="collapsed",
            key="app_lang_sel"
        )
        if sel_lang != cur_lang:
            st.session_state["ui_lang"] = sel_lang
            st.rerun()
    with c3:
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user_role"] = None
            st.rerun()

    # Route according to role
    if st.session_state["user_role"] == "patient":
        render_patient_portal()
    elif st.session_state["user_role"] == "doctor":
        render_admin_portal()

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
