"""
Module 0: Authentication & Role-Based Access Control UI
Lead: Student 1 (System Architect)
Part of Multimodal Fused Clinical Decision Support System (CDSS)
"""

import streamlit as st
from utils.auth_service import authenticate_user, register_user, load_users
from utils.medical_validator import validate_doctor_registration


def render_auth_page():
    """Renders the Sign In / Sign Up portal with role selection."""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 520px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }
        .auth-title {
            text-align: center;
            font-size: 1.6rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 6px;
        }
        .auth-subtitle {
            text-align: center;
            font-size: 0.9rem;
            color: #64748b;
            margin-bottom: 24px;
        }
        .demo-chip {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.82rem;
            cursor: pointer;
            text-align: center;
            margin-bottom: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 2, 1])

    with col_center:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 16px;">
                <span style="font-size: 2.8rem;">🩺</span>
                <div class="auth-title">Multimodal Fused Clinical Decision Support System</div>
                <div class="auth-subtitle">Point-of-Care Clinical Triage & Remote Doctor Tele-ICU</div>
            </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up (New Patient / Doctor)"])

        with tab_signin:
            st.markdown("##### Sign in to your account")
            login_username = st.text_input("Username or Email:", key="login_username_input").strip()
            login_password = st.text_input("Password:", type="password", key="login_password_input")

            if st.button("🚀 Access Portal", type="primary", use_container_width=True, key="btn_signin_submit"):
                if not login_username or not login_password:
                    st.error("Please enter both username and password.")
                else:
                    success, user_data, msg = authenticate_user(login_username, login_password)
                    if success:
                        st.session_state["authenticated"] = True
                        st.session_state["current_user"] = user_data
                        st.session_state["user_role"] = user_data.get("role", "patient")
                        st.toast(msg, icon="✅")
                        st.rerun()
                    else:
                        st.error(msg)

            st.divider()
            st.markdown("<p style='font-size: 0.82rem; font-weight: 600; color: #475569;'>⚡ Quick Demo Access (1-Click Viva Testing):</p>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("👨‍⚕️ Dr. Ramesh (Doctor)", use_container_width=True):
                    success, user_data, _ = authenticate_user("dr.ramesh", "doctor123")
                    st.session_state["authenticated"] = True
                    st.session_state["current_user"] = user_data
                    st.session_state["user_role"] = "doctor"
                    st.rerun()
            with col_d2:
                if st.button("🏠 Rajesh (Patient)", use_container_width=True):
                    success, user_data, _ = authenticate_user("patient.rajesh", "patient123")
                    st.session_state["authenticated"] = True
                    st.session_state["current_user"] = user_data
                    st.session_state["user_role"] = "patient"
                    st.rerun()

            if st.button("🤝 Sunita (ASHA Health Worker)", use_container_width=True):
                success, user_data, _ = authenticate_user("asha.sunita", "asha123")
                st.session_state["authenticated"] = True
                st.session_state["current_user"] = user_data
                st.session_state["user_role"] = "asha"
                st.rerun()

        with tab_signup:
            st.markdown("##### Create a new account")
            signup_role = st.selectbox(
                "Registering as:",
                ["patient", "doctor", "asha"],
                format_func=lambda x: "🏠 Patient / Home Care" if x == "patient" else ("👨‍⚕️ Doctor / Clinician" if x == "doctor" else "🤝 ASHA / Healthcare Worker")
            )
            
            full_name = st.text_input("Full Legal Name:", key="su_fullname")
            new_username = st.text_input("Choose Username:", key="su_username").strip()
            new_password = st.text_input("Choose Password (min 6 chars):", type="password", key="su_password")

            extra_meta = {}
            if signup_role == "patient":
                col_p1, col_p2 = st.columns(2)
                age = col_p1.number_input("Age:", min_value=1, max_value=110, value=35)
                gender = col_p2.selectbox("Gender:", ["Male", "Female", "Other"])
                phone = st.text_input("Mobile Phone Number:", key="su_phone", value="+91 ")
                location = st.text_input("PHC / Taluk Location:", value="Bantwal Rural PHC")
                emergency_contact = st.text_input("Emergency Contact Number:", value="+91 ")
                extra_meta = {
                    "age": age,
                    "gender": gender,
                    "phone": phone,
                    "location": location,
                    "emergency_contact": emergency_contact,
                    "patient_id": f"PT-2026-{1000 + len(load_users())}"
                }
            elif signup_role == "doctor":
                reg_num = st.text_input("State Medical Council Reg. No (e.g., KMC-12345):", value="KMC-")
                hospital = st.text_input("Hospital / Tele-ICU Center:", value="Bantwal District Hospital")
                email = st.text_input("Official Email:")
                extra_meta = {
                    "reg_number": reg_num,
                    "hospital": hospital,
                    "email": email
                }
            else: # asha
                sub_center = st.text_input("Sub-Center / Village Ward:", value="Panemangalore Sub-Center")
                worker_id = st.text_input("ASHA Worker ID:", value=f"ASHA-DK-{len(load_users()) + 100}")
                extra_meta = {
                    "sub_center": sub_center,
                    "worker_id": worker_id
                }

            if st.button("✨ Complete Registration", type="primary", use_container_width=True):
                if not full_name or not new_username or not new_password:
                    st.error("Please fill out all required fields.")
                elif signup_role == "doctor":
                    is_valid_reg, reg_msg, reg_details = validate_doctor_registration(reg_num)
                    if not is_valid_reg:
                        st.error(f"❌ Statutory Verification Failed: {reg_msg}")
                    else:
                        extra_meta["statutory_verification"] = reg_details
                        success, msg = register_user(
                            username=new_username,
                            password=new_password,
                            role=signup_role,
                            full_name=full_name,
                            extra_meta=extra_meta
                        )
                        if success:
                            st.success(f"{msg} ({reg_msg})")
                            st.info("You can now switch to the 'Sign In' tab to log in.")
                        else:
                            st.error(msg)
                else:
                    success, msg = register_user(
                        username=new_username,
                        password=new_password,
                        role=signup_role,
                        full_name=full_name,
                        extra_meta=extra_meta
                    )
                    if success:
                        st.success(msg)
                        st.info("You can now switch to the 'Sign In' tab to log in.")
                    else:
                        st.error(msg)
