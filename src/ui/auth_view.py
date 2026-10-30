"""
Module 0: Authentication & Role-Based Access Control UI
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Security Architecture:
  - Multi-Step Verification: Username & 10-Digit Mobile verification followed by role challenge
  - Doctor Gatekeeper: Confidential Medical Council Registration required for doctor accounts
  - Strict Input Guardrails: Full Name (letters only, no numbers), 10-Digit Mobile (6-9 prefix)
  - GPS Geolocation & Demographic Address Persistence (Auto-detect & Manual entry)
  - Cryptographic Bcrypt Salted Password Hashing (12 work rounds)
  - Brute-Force Rate Limiting (5 attempts / 15-minute lockouts)
  - Immutable Security & Clinical Access Audit Logging
"""

import streamlit as st
import time
from src.security.database import (
    get_user_by_identifier,
    get_user_by_username,
    verify_password,
    record_login_attempt,
    is_account_locked,
    create_user,
    get_audit_logs,
    fetch_location_by_gps,
    verify_doctor_phone_match
)
from src.security.guardrails import (
    validate_full_name,
    validate_phone_number,
    validate_email,
    validate_pincode,
    validate_doctor_reg,
    validate_password,
    RECOGNIZED_COUNCILS
)


def render_auth_page():
    """Renders the secure Sign In / Sign Up portal with multi-step verification, GPS auto-detect, and database persistence."""
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
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }
        .verified-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 5px solid #0284c7;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 16px;
        }
        .step-indicator {
            display: inline-block;
            background: #e0f2fe;
            color: #0369a1;
            font-size: 0.76rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 12px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 2.2, 1])

    with col_center:
        # Clean Header - Removed subtitle banner and security pills per user specification
        st.markdown("""
            <div style="text-align: center; margin-bottom: 24px;">
                <span style="font-size: 3rem;">🩺</span>
                <div class="auth-title">MEDFUSE-AI POINT-OF-CARE</div>
            </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_signup, tab_security_audit = st.tabs([
            "🔑 Sign In",
            "📝 Sign Up (Create Account)",
            "🛡️ Security & Audit Trail"
        ])

        # -----------------------------------------------------------------
        # 1. MULTI-STEP SIGN IN TAB
        # -----------------------------------------------------------------
        with tab_signin:
            # Manage 2-step verification state
            if "auth_login_step" not in st.session_state:
                st.session_state["auth_login_step"] = 1
            if "auth_target_user" not in st.session_state:
                st.session_state["auth_target_user"] = None

            # -------------------------------------------------------------
            # STEP 1: Username & 10-Digit Mobile Number Verification
            # -------------------------------------------------------------
            if st.session_state["auth_login_step"] == 1:
                st.markdown("<span class='step-indicator'>STEP 1 OF 2: IDENTITY VERIFICATION</span>", unsafe_allow_html=True)
                st.markdown("##### Sign In to Point-of-Care Portal")

                login_username = st.text_input(
                    "Username:",
                    placeholder="e.g. dr.ramesh, dr.priya, patient.rajesh",
                    key="login_step1_username"
                ).strip()

                login_phone = st.text_input(
                    "10-Digit Registered Mobile Number:",
                    placeholder="e.g. 9845012345",
                    key="login_step1_phone"
                ).strip()

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                if st.button("Verify & Proceed ➡️", type="primary", use_container_width=True, key="btn_login_step1"):
                    if not login_username:
                        st.error("⚠️ Please enter your registered username.")
                    elif not login_phone:
                        st.error("⚠️ Please enter your registered 10-digit mobile number.")
                    else:
                        # 1. Validate Mobile Number format
                        is_valid_phone, phone_err, cleaned_phone = validate_phone_number(login_phone)
                        if not is_valid_phone:
                            st.error(f"⚠️ Mobile Number Error: {phone_err}")
                        else:
                            # 2. Check user account in SQLite database
                            user = get_user_by_username(login_username)
                            if not user:
                                user = get_user_by_identifier(login_username)

                            if not user:
                                st.error(f"❌ No registered account found with username '{login_username}'. Please verify your username or sign up for a new account.")
                            else:
                                # 3. Check Brute-Force Rate Limiter Lockout
                                is_locked, lock_msg = is_account_locked(user)
                                if is_locked:
                                    st.error(lock_msg)
                                else:
                                    # 4. Check if entered phone strictly matches the registered phone in database
                                    user_phone = "".join(c for c in (user.get("phone") or "") if c.isdigit())
                                    if user_phone.startswith("91") and len(user_phone) == 12:
                                        user_phone = user_phone[2:]

                                    if cleaned_phone != user_phone:
                                        attempts, locked_now, msg = record_login_attempt(user["username"], is_success=False)
                                        if locked_now:
                                            st.error(msg)
                                        else:
                                            st.error("❌ The mobile number entered does not match the registered contact on file for this account.")
                                    else:
                                        # Phone matched successfully! Advance to Step 2
                                        st.session_state["auth_target_user"] = user
                                        st.session_state["auth_login_step"] = 2
                                        st.rerun()

            # -------------------------------------------------------------
            # STEP 2: Role-Gated Security Challenge & Password Verification
            # -------------------------------------------------------------
            elif st.session_state["auth_login_step"] == 2:
                user = st.session_state.get("auth_target_user")
                if not user:
                    st.session_state["auth_login_step"] = 1
                    st.rerun()

                user_role = user.get("role", "patient")

                st.markdown("<span class='step-indicator'>STEP 2 OF 2: CREDENTIAL CHALLENGE</span>", unsafe_allow_html=True)

                # Show verified identity card
                st.markdown(f"""
                    <div class="verified-box">
                        <div style="font-size: 0.74rem; font-weight: 700; color: #0284c7; text-transform: uppercase;">
                            ✓ Verified Identity
                        </div>
                        <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-top: 2px;">
                            {user.get('full_name')}
                        </div>
                        <div style="font-size: 0.82rem; color: #475569; margin-top: 3px;">
                            Username: <code>{user.get('username')}</code> &nbsp;•&nbsp; Mobile: <code>+91 {user.get('phone')}</code>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # ---------------------------------------------------------
                # DOCTOR CHALLENGE: Demands Medical Council Reg No + Password
                # ---------------------------------------------------------
                if user_role == "doctor":
                    st.markdown("##### Certified Practitioner Authentication")
                    st.caption("Doctor accounts require Medical Council registration verification to prevent unauthorized access.")

                    doc_council_input = st.text_input(
                        "Medical Council Registration Number (NMC / State Council):",
                        placeholder="e.g. KMC-58291, MMC-41209",
                        key="login_step2_council_reg"
                    ).strip()

                    doc_password = st.text_input(
                        "Doctor Account Password:",
                        type="password",
                        placeholder="Enter your confidential account password",
                        key="login_step2_doc_password"
                    )

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                    col_s2_submit, col_s2_back = st.columns([1.5, 1])

                    with col_s2_submit:
                        if st.button("🔐 Verify Doctor Credentials", type="primary", use_container_width=True, key="btn_login_step2_doc"):
                            if not doc_council_input:
                                st.error("⚠️ Please enter your Medical Council Registration Number.")
                            elif not doc_password:
                                st.error("⚠️ Please enter your password.")
                            else:
                                # Check lockout
                                is_locked, lock_msg = is_account_locked(user)
                                if is_locked:
                                    st.error(lock_msg)
                                else:
                                    # Normalize and compare Council Reg Number
                                    clean_entered_reg = doc_council_input.upper().replace(" ", "").replace("-", "")
                                    clean_db_reg = (user.get("reg_number") or "").upper().replace(" ", "").replace("-", "")

                                    if clean_entered_reg != clean_db_reg:
                                        attempts, locked_now, msg = record_login_attempt(user["username"], is_success=False)
                                        if locked_now:
                                            st.error(msg)
                                        else:
                                            st.error(f"❌ Medical Council Registration Number does not match official credentials on file for Dr. {user['full_name']}.")
                                    else:
                                        # Verify Bcrypt password
                                        if not verify_password(doc_password, user["password_hash"]):
                                            attempts, locked_now, msg = record_login_attempt(user["username"], is_success=False)
                                            if locked_now:
                                                st.error(msg)
                                            else:
                                                st.error(f"❌ Incorrect password. Failed attempt {attempts} of 5.")
                                        else:
                                            # Authenticated!
                                            record_login_attempt(user["username"], is_success=True)
                                            st.session_state["authenticated"] = True
                                            st.session_state["current_user"] = user
                                            st.session_state["user_role"] = "doctor"
                                            st.session_state["user_id"] = f"{user['full_name']} ({user['reg_number'] or 'RMP'})"
                                            st.session_state["last_activity"] = time.time()
                                            st.session_state["auth_login_step"] = 1
                                            st.session_state["auth_target_user"] = None
                                            st.toast(f"Welcome, Dr. {user['full_name']}! Authentication successful.", icon="✅")
                                            st.rerun()

                    with col_s2_back:
                        if st.button("← Change Account", use_container_width=True, key="btn_login_back_doc"):
                            st.session_state["auth_login_step"] = 1
                            st.session_state["auth_target_user"] = None
                            st.rerun()

                # ---------------------------------------------------------
                # NON-DOCTOR CHALLENGE: Only asks for Password
                # (Patients/public users never see doctor council fields)
                # ---------------------------------------------------------
                else:
                    portal_label = "Frontline Field Console" if user_role == "asha" else "Patient Portal"
                    st.markdown(f"##### Sign In to {portal_label}")

                    user_password = st.text_input(
                        "Account Password:",
                        type="password",
                        placeholder="Enter your account password",
                        key="login_step2_user_password"
                    )

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                    col_s2_submit, col_s2_back = st.columns([1.5, 1])

                    with col_s2_submit:
                        btn_label = "🚀 Sign In to Field Console" if user_role == "asha" else "🚀 Sign In to Patient Portal"
                        if st.button(btn_label, type="primary", use_container_width=True, key="btn_login_step2_user"):
                            if not user_password:
                                st.error("⚠️ Please enter your password.")
                            else:
                                # Check lockout
                                is_locked, lock_msg = is_account_locked(user)
                                if is_locked:
                                    st.error(lock_msg)
                                else:
                                    # Verify Bcrypt password
                                    if not verify_password(user_password, user["password_hash"]):
                                        attempts, locked_now, msg = record_login_attempt(user["username"], is_success=False)
                                        if locked_now:
                                            st.error(msg)
                                        else:
                                            st.error(f"❌ Incorrect password. Failed attempt {attempts} of 5.")
                                    else:
                                        # Authenticated!
                                        record_login_attempt(user["username"], is_success=True)
                                        st.session_state["authenticated"] = True
                                        st.session_state["current_user"] = user
                                        st.session_state["user_role"] = user_role

                                        if user_role == "asha":
                                            st.session_state["user_id"] = f"{user['full_name']} ({user['reg_number'] or 'ASHA Field Lead'})"
                                        else:
                                            st.session_state["user_id"] = f"{user['full_name']} (+91 {user['phone']})"

                                        st.session_state["last_activity"] = time.time()
                                        st.session_state["auth_login_step"] = 1
                                        st.session_state["auth_target_user"] = None
                                        st.toast(f"Welcome, {user['full_name']}! Authentication successful.", icon="✅")
                                        st.rerun()

                    with col_s2_back:
                        if st.button("← Change Account", use_container_width=True, key="btn_login_back_user"):
                            st.session_state["auth_login_step"] = 1
                            st.session_state["auth_target_user"] = None
                            st.rerun()

        # -----------------------------------------------------------------
        # 2. COMPREHENSIVE SIGN UP TAB (WITH GPS & STRICT VALIDATIONS)
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

            # ---------------- Personal & Contact Details ----------------
            st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 10px; margin-bottom: 4px;'>Personal & Contact Information</div>", unsafe_allow_html=True)

            # Full Name (Letters only - Strictly validated)
            new_name = st.text_input(
                "Full Name (Alphabetic letters & spaces only):",
                placeholder="e.g. Ananya Rao",
                key="signup_name_input"
            ).strip()

            # 10-Digit Mobile Contact (Strictly validated)
            new_phone = st.text_input(
                "Mobile Contact (10-Digit Indian Mobile Number):",
                placeholder="e.g. 9845012345",
                key="signup_phone_input"
            ).strip()

            new_email = st.text_input(
                "Email Address (Optional):",
                placeholder="e.g. ananya.rao@hospital.org",
                key="signup_email_input"
            ).strip()

            col_age, col_gen = st.columns(2)
            with col_age:
                new_age = st.number_input("Age:", min_value=1, max_value=120, value=35, step=1, key="signup_age_input")
            with col_gen:
                new_gender = st.selectbox("Gender:", ["Male", "Female", "Other", "Prefer not to disclose"], key="signup_gender_input")

            # ---------------- Role-Specific Information ----------------
            doc_reg_val = None
            doc_spec_val = None
            hosp_val = None
            doc_exp_val = None
            patient_blood_group = None
            patient_emg_name = None
            patient_emg_phone = None
            asha_id_val = None

            if "Doctor" in role_choice:
                st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>Doctor Medical Council Credentials</div>", unsafe_allow_html=True)
                doc_reg_val = st.text_input(
                    "State Medical Council / NMC Registration Number:",
                    placeholder="e.g. KMC-58291, MMC-41209, or NMC-2024-1234",
                    key="signup_doc_reg"
                ).strip()

                col_spec, col_exp = st.columns([1.5, 1])
                with col_spec:
                    doc_spec_val = st.selectbox(
                        "Clinical Specialization:",
                        [
                            "Pulmonology & Critical Care",
                            "Thoracic Radiology",
                            "General Medicine / Internal Medicine",
                            "Emergency & Trauma Medicine",
                            "Cardiology & Tele-ICU",
                            "Pediatric Pulmonology",
                            "Other Medical Specialization"
                        ],
                        key="signup_doc_spec"
                    )
                with col_exp:
                    doc_exp_val = st.number_input("Experience (Years):", min_value=0, max_value=60, value=8, step=1, key="signup_doc_exp")

                hosp_val = st.text_input(
                    "Hospital / Clinical Tele-ICU Center:",
                    placeholder="e.g. Bantwal District Hospital",
                    value="Bantwal District Hospital",
                    key="signup_doc_hosp"
                ).strip()

            elif "Patient" in role_choice:
                st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>Patient Clinical Demographics</div>", unsafe_allow_html=True)
                patient_blood_group = st.selectbox("Blood Group:", ["Unknown / Not Tested", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], key="signup_blood_group")

                col_emg1, col_emg2 = st.columns(2)
                with col_emg1:
                    patient_emg_name = st.text_input("Emergency Contact Person:", placeholder="e.g. Suresh Kumar (Brother)", key="signup_emg_name").strip()
                with col_emg2:
                    patient_emg_phone = st.text_input("Emergency Contact Mobile:", placeholder="e.g. 9448199999", key="signup_emg_phone").strip()

            elif "ASHA" in role_choice:
                st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>ASHA Field Identification</div>", unsafe_allow_html=True)
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

            # ---------------- Location & Geolocation Section ----------------
            st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>Address & Location (GPS Auto-Detection or Manual)</div>", unsafe_allow_html=True)

            # GPS Auto-detect button
            col_gps_btn, col_gps_stat = st.columns([1.2, 2])
            with col_gps_btn:
                if st.button("📍 Auto-Detect Location (GPS)", use_container_width=True, key="btn_detect_gps"):
                    loc = fetch_location_by_gps()
                    st.session_state["signup_loc_city"] = loc.get("city", "Mangaluru")
                    st.session_state["signup_loc_state"] = loc.get("state", "Karnataka")
                    st.session_state["signup_loc_pincode"] = loc.get("pincode", "575007")
                    st.session_state["signup_loc_coords"] = loc.get("gps_coordinates", "12.9187° N, 74.8598° E")
                    st.session_state["signup_gps_triggered"] = True
                    st.rerun()

            with col_gps_stat:
                if st.session_state.get("signup_gps_triggered", False):
                    st.markdown(f"<div style='font-size: 0.82rem; color: #166534; font-weight: 600; padding-top: 8px;'>✓ GPS Acquired: {st.session_state.get('signup_loc_city', '')}, {st.session_state.get('signup_loc_state', '')} ({st.session_state.get('signup_loc_coords', '')})</div>", unsafe_allow_html=True)
                else:
                    st.caption("Click button above to auto-fill address from GPS, or enter manually below.")

            address_street = st.text_input(
                "Street Address / House No / Locality:",
                placeholder="e.g. Main Hospital Road, Zone 2",
                key="signup_addr_street"
            ).strip()

            col_c1, col_c2 = st.columns(2)
            with col_c1:
                address_city = st.text_input(
                    "City / Town:",
                    value=st.session_state.get("signup_loc_city", "Bantwal"),
                    key="signup_addr_city"
                ).strip()
            with col_c2:
                address_state = st.text_input(
                    "State / Region:",
                    value=st.session_state.get("signup_loc_state", "Karnataka"),
                    key="signup_addr_state"
                ).strip()

            col_pin, col_coord = st.columns(2)
            with col_pin:
                address_pincode = st.text_input(
                    "Postal Pincode (6 Digits):",
                    value=st.session_state.get("signup_loc_pincode", "574211"),
                    key="signup_addr_pincode"
                ).strip()
            with col_coord:
                gps_coords = st.text_input(
                    "GPS Coordinates (Lat/Long):",
                    value=st.session_state.get("signup_loc_coords", "12.8913° N, 75.0347° E"),
                    key="signup_addr_coords"
                ).strip()

            # ---------------- Security Credentials ----------------
            st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>Account Password & Security</div>", unsafe_allow_html=True)
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

                # 1. Full Name Validation (Strictly reject numbers, digits, symbols)
                valid_name, name_err = validate_full_name(new_name)
                if not valid_name:
                    st.error(f"⚠️ Full Name Validation Error: {name_err}")
                    st.stop()

                # 2. Mobile Number Validation (Strictly 10 digits, starts 6-9)
                valid_phone, phone_err, cleaned_phone = validate_phone_number(new_phone)
                if not valid_phone:
                    st.error(f"⚠️ Mobile Phone Validation Error: {phone_err}")
                    st.stop()

                # 3. Email Validation (if provided)
                if new_email:
                    valid_email, email_err = validate_email(new_email)
                    if not valid_email:
                        st.error(f"⚠️ Email Error: {email_err}")
                        st.stop()

                # 4. Postal Pincode Validation
                if address_pincode:
                    valid_pin, pin_err = validate_pincode(address_pincode)
                    if not valid_pin:
                        st.error(f"⚠️ Postal Pincode Error: {pin_err}")
                        st.stop()

                # 5. Role-specific validations
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

                # 6. Password Strength and Confirm Password Matching
                valid_pw, pw_err = validate_password(new_pw, confirm_pw)
                if not valid_pw:
                    st.error(f"⚠️ Password Security Error: {pw_err}")
                    st.stop()

                # ================= DATABASE INSERTION =================
                # Generate unique clean username
                clean_name_parts = [p.lower() for p in new_name.split() if p.isalpha()]
                first_name_str = clean_name_parts[0] if clean_name_parts else "user"
                if role_code == "doctor":
                    username_candidate = f"dr.{first_name_str}_{cleaned_phone[-4:]}"
                elif role_code == "asha":
                    username_candidate = f"asha.{first_name_str}_{cleaned_phone[-4:]}"
                else:
                    username_candidate = f"patient.{first_name_str}_{cleaned_phone[-4:]}"

                success, msg, created_user_record = create_user(
                    username=username_candidate,
                    password=new_pw,
                    full_name=new_name,
                    role=role_code,
                    phone=cleaned_phone,
                    reg_number=doc_reg_val,
                    organization=hosp_val,
                    email=new_email if new_email else None,
                    age=int(new_age),
                    gender=new_gender,
                    address=address_street if address_street else None,
                    city=address_city if address_city else None,
                    state=address_state if address_state else None,
                    pincode=address_pincode if address_pincode else None,
                    gps_coordinates=gps_coords if gps_coords else None,
                    emergency_contact_name=patient_emg_name if patient_emg_name else None,
                    emergency_contact_phone=patient_emg_phone if patient_emg_phone else None,
                    specialization=doc_spec_val if doc_spec_val else None,
                    experience_years=int(doc_exp_val) if doc_exp_val else None,
                    blood_group=patient_blood_group if patient_blood_group else None
                )

                if not success:
                    st.error(f"❌ Registration Error: {msg}")
                else:
                    # Authenticate newly created user immediately
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

                    st.success(f"🎉 Account successfully created for {new_name}! Username: '{username_candidate}'. Redirecting...")
                    time.sleep(1.0)
                    st.rerun()

        # -----------------------------------------------------------------
        # 3. SECURITY & AUDIT TRAIL TAB
        # -----------------------------------------------------------------
        with tab_security_audit:
            st.markdown("##### 🛡️ Clinical Security & Authentication Audit Trail")
            st.caption("Immutable system audit logs recorded in SQLite database:")

            recent_logs = get_audit_logs(limit=12)
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
                <div style="font-size: 0.78rem; color: #64748b; line-height: 1.6;">
                    • <strong>Bcrypt Adaptive Hashing:</strong> Work factor = 12 rounds.<br/>
                    • <strong>Brute-Force Rate Limiting:</strong> Enforces temporary 15-minute lockouts upon 5 consecutive failed login attempts.<br/>
                    • <strong>Identity Guardrails:</strong> Full Names validated strictly against alphabetic characters (digits rejected).<br/>
                    • <strong>Indian Mobile Standard:</strong> Validates 10 digits starting with 6, 7, 8, or 9.<br/>
                    • <strong>Doctor Gatekeeper:</strong> Certified RMP accounts require Medical Council registration verification.
                </div>
            """, unsafe_allow_html=True)


__all__ = ["render_auth_page"]
