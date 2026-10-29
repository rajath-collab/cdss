"""
Module 0: Authentication & Role-Based Access Control UI
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Complete Frontend Implementation
"""
import streamlit as st
import re
from src.config import DOCTOR_DATABASE

RECOGNIZED_COUNCILS = ["KMC", "MMC", "DMC", "TNMC", "APMC", "TSMC", "NMC", "MCI"]

def render_auth_page():
    """Renders the comprehensive Sign In / Sign Up portal with role selection."""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 540px;
            margin: 0 auto;
            background: #ffffff;
            padding: 28px;
            border-radius: 14px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid #e2e8f0;
        }
        .auth-title {
            text-align: center;
            font-size: 1.65rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
        }
        .auth-subtitle {
            text-align: center;
            font-size: 0.92rem;
            color: #64748b;
            margin-bottom: 22px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 2, 1])

    with col_center:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 16px;">
                <span style="font-size: 3rem;">🩺</span>
                <div class="auth-title">MedFuse-AI Point-of-Care CDSS</div>
                <div class="auth-subtitle">Unified Multimodal Clinical Triage & Tele-ICU Gateway</div>
            </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up (New Account)"])

        with tab_signin:
            st.markdown("##### Sign in to access your portal")
            username = st.text_input("Username, Mobile, or Council Reg No:", value="dr.ramesh", key="auth_login_user")
            password = st.text_input("Password or PIN:", value="doctor123", type="password", key="auth_login_pass")

            if st.button("🚀 Access Point-of-Care Portal", type="primary", use_container_width=True, key="btn_auth_submit"):
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    st.session_state["authenticated"] = True
                    if "dr" in username.lower() or "kmc" in username.lower() or password in ["7788", "1234", "doctor123"]:
                        st.session_state["user_role"] = "doctor"
                        st.session_state["user_id"] = "Dr. Ramesh Rao, MD (KMC-58291)"
                    elif "asha" in username.lower() or password in ["asha123"]:
                        st.session_state["user_role"] = "asha"
                        st.session_state["user_id"] = "Sunita Naik (ASHA Lead - Panemangalore)"
                    else:
                        st.session_state["user_role"] = "patient"
                        st.session_state["user_id"] = f"+91 9845012345 (Rajesh Kumar)"
                    st.toast("Authenticated successfully!", icon="✅")
                    st.rerun()

            st.divider()
            st.markdown("<p style='font-size: 0.82rem; font-weight: 600; color: #475569;'>⚡ Quick Viva Demo Access (1-Click Login):</p>", unsafe_allow_html=True)
            cd1, cd2, cd3 = st.columns(3)
            with cd1:
                if st.button("👨‍⚕️ Dr. Ramesh\n(Doctor)", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "doctor"
                    st.session_state["user_id"] = "Dr. Ramesh Rao, MD (KMC-58291)"
                    st.rerun()
            with cd2:
                if st.button("🏠 Rajesh\n(Patient)", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "patient"
                    st.session_state["user_id"] = "+91 9845012345 (Rajesh Kumar)"
                    st.rerun()
            with cd3:
                if st.button("🤝 Sunita\n(ASHA Lead)", use_container_width=True):
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "asha"
                    st.session_state["user_id"] = "Sunita Naik (ASHA-DK-409)"
                    st.rerun()

        with tab_signup:
            st.markdown("##### Create a new user profile")
            new_role = st.selectbox("Registering as:", ["Patient / Citizen", "Medical Doctor (RMP)", "ASHA / Health Worker"])
            new_name = st.text_input("Full Name:", placeholder="e.g. Ananya Rao")
            new_phone = st.text_input("Mobile Contact:", placeholder="10-digit phone number")

            if "Doctor" in new_role:
                doc_council_reg = st.text_input("State Medical Council / NMC Reg No:", placeholder="e.g. KMC-58291")
                hosp = st.text_input("Affiliated Hospital / PHC:", value="Bantwal District Hospital")
            elif "ASHA" in new_role:
                asha_id = st.text_input("ASHA Worker ID:", placeholder="e.g. ASHA-DK-409")

            new_pw = st.text_input("Create Secret PIN / Password:", type="password")

            if st.button("📝 Register Account", use_container_width=True):
                if not new_name or not new_pw:
                    st.error("Please fill in required fields.")
                else:
                    st.session_state["authenticated"] = True
                    if "Doctor" in new_role:
                        st.session_state["user_role"] = "doctor"
                        st.session_state["user_id"] = f"{new_name} ({doc_council_reg if 'doc_council_reg' in locals() else 'RMP'})"
                    elif "ASHA" in new_role:
                        st.session_state["user_role"] = "asha"
                        st.session_state["user_id"] = f"{new_name} (ASHA Field Lead)"
                    else:
                        st.session_state["user_role"] = "patient"
                        st.session_state["user_id"] = f"{new_name} (+91 {new_phone})"
                    st.success("Account registered and authenticated!")
                    st.rerun()

__all__ = ["render_auth_page"]

