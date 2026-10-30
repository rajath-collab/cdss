"""
Module 0: Authentication & Role-Based Access Control UI
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Security Implementation:
  - SQLite Transactional Database Persistence
  - Cryptographic Bcrypt Password Hashing (12 rounds)
  - Strict Full Name Validation (letters only, no numbers allowed)
  - Strict 10-Digit Mobile Phone Validation (6-9 prefix, no arbitrary strings)
  - Confirm Password Verification on Account Creation
  - Brute-Force Rate Limiting (5 attempts with 15-minute lockout)
  - Tamper-Evident Security Audit Logging
"""

import streamlit as st
import time
from src.security.database import (
    get_user_by_identifier,
    verify_password,
    record_login_attempt,
    is_account_locked,
    create_user,
    get_audit_logs
)
from src.security.guardrails import (
    validate_full_name,
    validate_phone_number,
    validate_doctor_reg,
    validate_password,
    RECOGNIZED_COUNCILS
)


def render_auth_page():
    """Renders the secure Sign In / Sign Up portal with strict validation and database authentication."""
    st.markdown("""
        <style>
        .auth-card {
            background: #ffffff;
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
        }
        .auth-title {
            text-align: center;
            font-size: 1.7rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        }
        .auth-subtitle {
            text-align: center;
            font-size: 0.92rem;
            color: #64748b;
            margin-bottom: 22px;
        }
        .sec-pill {
            display: inline-block;
            background: #f1f5f9;
            color: #475569;
            border: 1px solid #cbd5e1;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.74rem;
            font-weight: 600;
            margin: 2px 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 18px;">
                <span style="font-size: 3rem;">🩺</span>
                <div class="auth-title">MEDFUSE-AI POINT-OF-CARE</div>
                <div class="auth-subtitle">
                    Secure Healthcare Gateway • Role-Based Clinical Access Control
                </div>
                <div style="margin-bottom: 15px;">
                    <span class="sec-pill">🔒 Bcrypt Salted Hashing</span>
                    <span class="sec-pill">🛡️ Brute-Force Rate Limiter</span>
                    <span class="sec-pill">💾 SQLite ACID Database</span>
                    <span class="sec-pill">📜 DPDP Act & HIPAA Compliant</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_signup, tab_security_audit = st.tabs([
            "🔑 Sign In",
            "📝 Sign Up (Create Account)",
            "🛡️ Security & Audit Trail"
        ])

        # -----------------------------------------------------------------
        # 1. SECURE SIGN IN TAB
        # -----------------------------------------------------------------
        with tab_signin:
            st.markdown("##### Authorized Clinical Sign In")
            login_id = st.text_input(
                "Username, 10-Digit Mobile Number, or Council Reg No:",
                placeholder="e.g. dr.ramesh, 9845012345, or KMC-58291",
                key="auth_login_identifier"
            ).strip()

            login_password = st.text_input(
                "Account Password:",
                type="password",
                placeholder="Enter your registered password",
                key="auth_login_password"
            )

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if st.button("🚀 Sign In to Portal", type="primary", use_container_width=True, key="btn_signin_submit"):
                if not login_id:
                    st.error("⚠️ Please enter your registered username, mobile number, or registration number.")
                elif not login_password:
                    st.error("⚠️ Please enter your password.")
                else:
                    # Query user from SQLite database
                    user = get_user_by_identifier(login_id)
                    if not user:
                        st.error(f"❌ No registered user found matching identifier '{login_id}'. Please check your entry or create a new account.")
                    else:
                        # 1. Check account lockout guard (Brute-Force Protection)
                        is_locked, lock_msg = is_account_locked(user)
                        if is_locked:
                            st.error(lock_msg)
                        else:
                            # 2. Cryptographic password verification (Bcrypt)
                            is_valid = verify_password(login_password, user["password_hash"])
                            if not is_valid:
                                attempts, locked_now, msg = record_login_attempt(user["username"], is_success=False)
                                if locked_now:
                                    st.error(msg)
                                else:
                                    st.error(f"❌ Incorrect password for user '{user['username']}'. Failed attempt {attempts} of 5. After 5 failed attempts, your account will be locked for 15 minutes.")
                            else:
                                # 3. Password verified successfully!
                                record_login_attempt(user["username"], is_success=True)

                                # Set session state
                                st.session_state["authenticated"] = True
                                st.session_state["current_user"] = user
                                st.session_state["user_role"] = user["role"]
                                
                                # Format display name nicely according to role
                                if user["role"] == "doctor":
                                    display_name = f"{user['full_name']} ({user['reg_number'] or 'RMP'})"
                                elif user["role"] == "asha":
                                    display_name = f"{user['full_name']} ({user['reg_number'] or 'ASHA Field Lead'})"
                                else:
                                    display_name = f"{user['full_name']} (+91 {user['phone']})"

                                st.session_state["user_id"] = display_name
                                st.session_state["last_activity"] = time.time()

                                st.toast(f"Welcome, {user['full_name']}! Authentication successful.", icon="✅")
                                st.rerun()

            st.caption("ℹ️ Clinical Security Note: Passwords are encrypted with Bcrypt (12 work rounds). All authentication events are recorded in the security audit database.")

        # -----------------------------------------------------------------
        # 2. SECURE SIGN UP TAB (WITH STRICT VALIDATIONS & CONFIRM PASSWORD)
        # -----------------------------------------------------------------
        with tab_signup:
            st.markdown("##### Create a New Clinical or Patient Account")

            role_choice = st.selectbox(
                "Select User Role:",
                [
                    "👤 Patient / Citizen",
                    "👨‍⚕️ Medical Doctor (Certified RMP)",
                    "🤝 ASHA / Frontline Health Worker"
                ],
                key="signup_role_select"
            )

            # 1. Full Name input (Letters only - Strictly validated)
            new_name = st.text_input(
                "Full Name (Alphabetic letters & spaces only):",
                placeholder="e.g. Ananya Rao",
                key="signup_name_input"
            ).strip()

            # 2. 10-Digit Mobile Contact input (Strictly validated)
            new_phone = st.text_input(
                "Mobile Contact (10-Digit Indian Mobile Number):",
                placeholder="e.g. 9845012345",
                key="signup_phone_input"
            ).strip()

            # Role-specific fields
            doc_reg_val = None
            hosp_val = None
            asha_id_val = None

            if "Doctor" in role_choice:
                st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #1e293b; margin-top: 6px;'>Doctor Medical Council Credentials:</div>", unsafe_allow_html=True)
                doc_reg_val = st.text_input(
                    "State Medical Council / NMC Registration No:",
                    placeholder="e.g. KMC-58291, MMC-41209, or NMC-2024-1234",
                    key="signup_doc_reg"
                ).strip()

                hosp_val = st.text_input(
                    "Hospital / PHC / Tele-ICU Center:",
                    placeholder="e.g. Bantwal District Hospital",
                    value="Bantwal District Hospital",
                    key="signup_doc_hosp"
                ).strip()

            elif "ASHA" in role_choice:
                st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #1e293b; margin-top: 6px;'>ASHA Worker Identification:</div>", unsafe_allow_html=True)
                asha_id_val = st.text_input(
                    "ASHA Worker ID / Sub-Center Code:",
                    placeholder="e.g. ASHA-DK-409",
                    key="signup_asha_id"
                ).strip()

                hosp_val = st.text_input(
                    "Primary Health Centre (PHC) Sub-Center:",
                    placeholder="e.g. Panemangalore PHC Sub-Center",
                    value="Panemangalore PHC Sub-Center",
                    key="signup_asha_hosp"
                ).strip()

            # 3. Password and Confirm Password inputs
            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #1e293b; margin-top: 6px;'>Security Credentials:</div>", unsafe_allow_html=True)
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                new_pw = st.text_input(
                    "Create Password (Min 6 chars):",
                    type="password",
                    placeholder="Enter password",
                    key="signup_pw1"
                )
            with col_p2:
                confirm_pw = st.text_input(
                    "Confirm Password:",
                    type="password",
                    placeholder="Re-enter password",
                    key="signup_pw2"
                )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if st.button("📝 Register & Create Secured Account", type="primary", use_container_width=True, key="btn_signup_submit"):
                # ================= VALIDATION PIPELINE =================
                
                # Check 1: Full Name Validation (Strictly reject numbers, digits, symbols)
                valid_name, name_err = validate_full_name(new_name)
                if not valid_name:
                    st.error(f"⚠️ Full Name Validation Error: {name_err}")
                    st.stop()

                # Check 2: Mobile Number Validation (Strictly 10 digits, starts 6-9)
                valid_phone, phone_err, cleaned_phone = validate_phone_number(new_phone)
                if not valid_phone:
                    st.error(f"⚠️ Mobile Phone Validation Error: {phone_err}")
                    st.stop()

                # Check 3: Role-specific validations
                role_code = "patient"
                if "Doctor" in role_choice:
                    role_code = "doctor"
                    valid_reg, reg_err, cleaned_reg = validate_doctor_reg(doc_reg_val)
                    if not valid_reg:
                        st.error(f"⚠️ Medical Council Registration Error: {reg_err}")
                        st.stop()
                    doc_reg_val = cleaned_reg
                elif "ASHA" in role_choice:
                    role_code = "asha"
                    if not asha_id_val or len(asha_id_val) < 3:
                        st.error("⚠️ ASHA Worker ID is required (minimum 3 characters).")
                        st.stop()
                    doc_reg_val = asha_id_val.upper()

                # Check 4: Password Strength and Confirm Password Matching
                valid_pw, pw_err = validate_password(new_pw, confirm_pw)
                if not valid_pw:
                    st.error(f"⚠️ Password Security Error: {pw_err}")
                    st.stop()

                # ================= DATABASE INSERTION =================
                # Generate unique username
                username_base = new_name.lower().replace(" ", ".")
                username_candidate = f"{username_base}_{cleaned_phone[-4:]}"

                success, msg, created_user_record = create_user(
                    username=username_candidate,
                    password=new_pw,
                    full_name=new_name,
                    role=role_code,
                    phone=cleaned_phone,
                    reg_number=doc_reg_val,
                    organization=hosp_val
                )

                if not success:
                    st.error(f"❌ Registration Error: {msg}")
                else:
                    # Authenticate newly created user immediately!
                    st.session_state["authenticated"] = True
                    st.session_state["current_user"] = created_user_record
                    st.session_state["user_role"] = role_code

                    if role_code == "doctor":
                        disp = f"{new_name} ({doc_reg_val})"
                    elif role_code == "asha":
                        disp = f"{new_name} ({doc_reg_val})"
                    else:
                        disp = f"{new_name} (+91 {cleaned_phone})"

                    st.session_state["user_id"] = disp
                    st.session_state["last_activity"] = time.time()

                    st.success("🎉 Account created and securely encrypted with Bcrypt! Redirecting to your portal...")
                    time.sleep(1.0)
                    st.rerun()

        # -----------------------------------------------------------------
        # 3. SECURITY & AUDIT TRAIL TAB (DEMONSTRATES WORKING SECURITY IMPLEMENTATION)
        # -----------------------------------------------------------------
        with tab_security_audit:
            st.markdown("##### 🛡️ Clinical Security & Authentication Audit Trail")
            st.caption("Immutable system audit logs recorded in SQLite complying with DPDP Act 2023 & HIPAA Security Rules:")

            recent_logs = get_audit_logs(limit=10)
            if recent_logs:
                for entry in recent_logs:
                    evt = entry.get("event_type", "EVENT")
                    badge_color = "#16a34a" if "SUCCESS" in evt or "REGISTER" in evt else ("#dc2626" if "LOCK" in evt or "FAIL" in evt else "#0284c7")
                    st.markdown(f"""
                        <div style="background: #f8fafc; border-left: 4px solid {badge_color}; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #0f172a; font-size: 0.88rem;">{evt}</strong>
                                <span style="font-size: 0.75rem; color: #64748b;">{entry.get('timestamp', '')}</span>
                            </div>
                            <div style="font-size: 0.82rem; color: #334155; margin-top: 3px;">
                                User: <code>{entry.get('username', 'SYSTEM')}</code> • {entry.get('details', '')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No audit logs recorded yet.")

            st.divider()
            st.markdown("""
                <div style="font-size: 0.78rem; color: #64748b; line-height: 1.5;">
                    • <strong>Bcrypt Adaptive Hashing:</strong> Work factor = 12 rounds.<br/>
                    • <strong>Brute-Force Rate Limiting:</strong> Enforces temporary 15-minute lockouts upon 5 consecutive failed login attempts.<br/>
                    • <strong>Identity Validation:</strong> Full Names validated against regex <code>^[A-Za-z\\s.'-]{{2,60}}$</code> (strictly no digits allowed).<br/>
                    • <strong>Indian Mobile Standard:</strong> Validates 10 digits starting with 6, 7, 8, or 9.
                </div>
            """, unsafe_allow_html=True)


__all__ = ["render_auth_page"]
