"""
Project: Multimodal Fused Clinical Decision Support System (CDSS)
Department: CSE (Data Science) | KIT Mangalore
Lead: Student 1 (Main Coder / System Architect)
"""
import streamlit as st
from src.config import init_session_state, DOCTOR_DATABASE
from src.ui.styles import CUSTOM_CSS
from src.ui.patient_view import render_patient_portal
from src.ui.admin_view import render_admin_portal

# 1. Page Config
st.set_page_config(page_title="MedFuse-AI | CDSS", page_icon="🩺", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_session_state()

# 2. Authentication Gateway
if not st.session_state["authenticated"]:
    st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <div style="font-size: 3rem;">🩺</div>
            <h1 style="color: #38BDF8; margin: 0;">CDSS-AI POINT-OF-CARE</h1>
        </div>
    """, unsafe_allow_html=True)

    tab_patient, tab_doctor = st.tabs(["👤 Patient / Home User", "👨‍⚕️ Clinician / Radiologist (Admin)"])

    with tab_patient:
        phone = st.text_input("Mobile Number:", placeholder="Enter 10-digit number")
        otp = st.text_input("OTP (Demo: 123456):", type="password")
        if st.button("Sign In as Patient", use_container_width=True):
            if otp == "123456":
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "patient"
                st.session_state["user_id"] = f"+91 {phone}" if phone else "Patient"
                st.rerun()
            else:
                st.error("Use demo OTP: 123456")

    with tab_doctor:
        doc_reg = st.selectbox("Medical Council Reg No:", list(DOCTOR_DATABASE.keys()))
        doc_pin = st.text_input("Doctor Security PIN (Demo: 7788):", type="password")
        if st.button("Authorize Clinician Console", use_container_width=True):
            if doc_pin == DOCTOR_DATABASE[doc_reg]["pin"]:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "doctor"
                st.session_state["user_id"] = f"{DOCTOR_DATABASE[doc_reg]['name']} ({doc_reg})"
                st.rerun()
            else:
                st.error("Invalid Doctor PIN. Enter 7788.")

# 3. Authenticated Router
else:
    # Top Bar
    c1, c2 = st.columns([5, 1])
    c1.markdown(f"**Logged in as:** `{st.session_state['user_id']}` ({st.session_state['user_role'].upper()})")
    if c2.button("🚪 Log Out"):
        st.session_state["authenticated"] = False
        st.session_state["user_role"] = None
        st.rerun()

    # Route according to role
    if st.session_state["user_role"] == "patient":
        render_patient_portal()
    elif st.session_state["user_role"] == "doctor":
        render_admin_portal()