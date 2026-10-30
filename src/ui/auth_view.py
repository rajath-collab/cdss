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
from src.ui.translations import get_ui_text, LANGUAGES


def render_auth_page():
    """Renders the secure Sign In / Sign Up portal with multi-step verification, GPS auto-detect, and database persistence."""
    ui_lang = st.session_state.get("ui_lang", "en")
    t = get_ui_text(ui_lang)
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
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border: 1px solid #cbd5e1; border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 2.2rem; line-height: 1;">🩺</span>
                    <div>
                        <div style="font-size: 1.45rem; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; line-height: 1.1;">MEDFUSE-AI</div>
                        <div style="font-size: 0.76rem; color: #64748b; font-weight: 600;">Multimodal Clinical Decision Support System</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Prominent Vernacular Language Selector Banner
        st.markdown(f"<div style='font-size: 0.8rem; font-weight: 800; color: #0284c7; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px;'>{t.get('lang_selector_label', '🌐 Portal Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:')}</div>", unsafe_allow_html=True)
        lang_keys = list(LANGUAGES.keys())
        cur_idx = lang_keys.index(ui_lang) if ui_lang in lang_keys else 0

        def _on_auth_lang_select():
            st.session_state["ui_lang"] = st.session_state["auth_lang_select_top"]

        st.selectbox(
            "Portal Language",
            lang_keys,
            index=cur_idx,
            format_func=lambda k: f"{LANGUAGES[k]['flag']} {LANGUAGES[k]['native']}",
            key="auth_lang_select_top",
            label_visibility="collapsed",
            on_change=_on_auth_lang_select
        )
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        tab_signin, tab_signup = st.tabs([
            t.get("auth_signin_tab", "🔑 Sign In"),
            t.get("auth_signup_tab", "📝 Sign Up (Create Account)")
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
                st.markdown(f"<span class='step-indicator'>{t.get('auth_step1_label', 'STEP 1 OF 2: IDENTITY VERIFICATION')}</span>", unsafe_allow_html=True)

                login_username = st.text_input(
                    t.get("auth_username_label", "Username:"),
                    placeholder=t.get("placeholder_username", "e.g. dr.ramesh, dr.priya, patient.rajesh"),
                    key="login_step1_username"
                ).strip()

                login_phone = st.text_input(
                    t.get("auth_mobile_label", "10-Digit Registered Mobile Number:"),
                    placeholder=t.get("placeholder_phone", "e.g. 9845012345"),
                    key="login_step1_phone"
                ).strip()

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                if st.button(t.get("auth_btn_verify", "Verify & Proceed ➡️"), type="primary", use_container_width=True, key="btn_login_step1"):
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

                st.markdown(f"<span class='step-indicator'>{t.get('auth_step2_label', 'STEP 2 OF 2: CREDENTIAL CHALLENGE')}</span>", unsafe_allow_html=True)

                # Show verified identity card
                st.markdown(f"""
                    <div class="verified-box">
                        <div style="font-size: 0.74rem; font-weight: 700; color: #0284c7; text-transform: uppercase;">
                            {t.get('auth_verified_identity', '✓ Verified Identity')}
                        </div>
                        <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-top: 2px;">
                            {user.get('full_name')}
                        </div>
                        <div style="font-size: 0.82rem; color: #475569; margin-top: 3px;">
                            {t.get('auth_username_tag', 'Username:')} <code>{user.get('username')}</code> &nbsp;•&nbsp; {t.get('auth_mobile_tag', 'Mobile:')} <code>+91 {user.get('phone')}</code>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # ---------------------------------------------------------
                # DOCTOR CHALLENGE: Demands Medical Council Reg No + Password
                # ---------------------------------------------------------
                if user_role == "doctor":
                    st.markdown(f"##### {t.get('auth_doc_chal_title', 'Certified Practitioner Authentication')}")
                    st.caption(t.get('auth_doc_chal_desc', 'Doctor accounts require Medical Council registration verification to prevent unauthorized access.'))

                    doc_council_input = st.text_input(
                        t.get("auth_doc_council_label", "Medical Council Registration Number (NMC / State Council):"),
                        placeholder="e.g. KMC-58291, MMC-41209",
                        key="login_step2_council_reg"
                    ).strip()

                    doc_password = st.text_input(
                        t.get("auth_doc_pw_label", "Doctor Account Password:"),
                        type="password",
                        placeholder="Enter your confidential account password",
                        key="login_step2_doc_password"
                    )

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                    col_s2_submit, col_s2_back = st.columns([1.5, 1])

                    with col_s2_submit:
                        if st.button(t.get("auth_btn_doc_login", "🔐 Verify Doctor Credentials"), type="primary", use_container_width=True, key="btn_login_step2_doc"):
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
                        if st.button(t.get("auth_btn_change_account", "← Change Account"), use_container_width=True, key="btn_login_back_doc"):
                            st.session_state["auth_login_step"] = 1
                            st.session_state["auth_target_user"] = None
                            st.rerun()

                # ---------------------------------------------------------
                # ADMIN CHALLENGE: Hospital Administrator Master Password
                # ---------------------------------------------------------
                elif user_role == "admin":
                    st.markdown("##### Hospital Administrator Authentication")
                    st.caption("Administrator credentials are required to manage hospital staff, patient master records, and clinical systems.")

                    admin_password = st.text_input(
                        t.get("auth_admin_pw_label", "Administrator Password:"),
                        type="password",
                        placeholder="Enter administrator password",
                        key="login_step2_admin_password"
                    )

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    col_s2_submit, col_s2_back = st.columns([1.5, 1])

                    with col_s2_submit:
                        if st.button(t.get("auth_btn_admin_login", "🔐 Verify & Enter Admin Portal"), type="primary", use_container_width=True, key="btn_login_step2_admin"):
                            if not admin_password:
                                st.error("⚠️ Please enter administrator password.")
                            else:
                                is_locked, lock_msg = is_account_locked(user)
                                if is_locked:
                                    st.error(lock_msg)
                                elif not verify_password(admin_password, user["password_hash"]):
                                    attempts, locked_now, msg = record_login_attempt(user["username"], is_success=False)
                                    if locked_now:
                                        st.error(msg)
                                    else:
                                        st.error(f"❌ Incorrect administrator password. Failed attempt {attempts} of 5.")
                                else:
                                    record_login_attempt(user["username"], is_success=True)
                                    st.session_state["authenticated"] = True
                                    st.session_state["current_user"] = user
                                    st.session_state["user_role"] = "admin"
                                    st.session_state["user_id"] = f"{user['full_name']} (Medical Superintendent)"
                                    st.session_state["last_activity"] = time.time()
                                    st.session_state["auth_login_step"] = 1
                                    st.session_state["auth_target_user"] = None
                                    st.toast(f"Welcome, {user['full_name']}! System governance portal unlocked.", icon="✅")
                                    st.rerun()

                    with col_s2_back:
                        if st.button(t.get("auth_btn_change_account", "← Change Account"), use_container_width=True, key="btn_login_back_admin"):
                            st.session_state["auth_login_step"] = 1
                            st.session_state["auth_target_user"] = None
                            st.rerun()

                # ---------------------------------------------------------
                # NON-DOCTOR / NON-ADMIN CHALLENGE: Only asks for Password
                # (Patients/public users never see doctor council or admin fields)
                # ---------------------------------------------------------
                else:
                    portal_label = t.get("role_asha", "Frontline Field Console") if user_role == "asha" else t.get("role_patient", "Patient Portal")
                    st.markdown(f"##### {t.get('auth_patient_chal_title', 'Sign In to Patient Portal')}")

                    user_password = st.text_input(
                        t.get("auth_user_pw_label", "Account Password:"),
                        type="password",
                        placeholder="Enter your account password",
                        key="login_step2_user_password"
                    )

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                    col_s2_submit, col_s2_back = st.columns([1.5, 1])

                    with col_s2_submit:
                        btn_label = t.get("auth_btn_field_login", "🚀 Sign In to Field Console") if user_role == "asha" else t.get("auth_btn_patient_login", "🚀 Sign In to Patient Portal")
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
                        if st.button(t.get("auth_btn_change_account", "← Change Account"), use_container_width=True, key="btn_login_back_user"):
                            st.session_state["auth_login_step"] = 1
                            st.session_state["auth_target_user"] = None
                            st.rerun()

        # -----------------------------------------------------------------
        # 2. COMPREHENSIVE SIGN UP TAB (WITH GPS & STRICT VALIDATIONS)
        # -----------------------------------------------------------------
        with tab_signup:
            st.markdown(f"##### {t.get('signup_title', 'Create a New Patient / Citizen Account')}")

            # Institutional Governance Notice Card (NMC & Hospital Security Mandate)
            st.markdown(f"""
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 5px solid #0284c7; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.88rem; display: flex; align-items: center; gap: 6px;">
                        <span>🔒</span> {t.get('signup_staff_notice_title', 'Public Registration: Patient & Citizen Health Records Only')}
                    </div>
                    <div style="font-size: 0.8rem; color: #475569; margin-top: 4px; line-height: 1.45;">
                        {t.get('signup_staff_notice_desc', 'Notice for Clinicians & Hospital Staff: Certified Medical Practitioner (RMP) and Hospital Administrator accounts are provisioned exclusively by the Hospital Medical Directorate. Self-registration for clinical staff is disabled per National Medical Commission (NMC) security mandates.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ---------------- Personal & Contact Details ----------------
            st.markdown(f"<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 10px; margin-bottom: 4px;'>{t.get('signup_personal_sec', 'Personal & Contact Information')}</div>", unsafe_allow_html=True)

            # Full Name (Letters only - Strictly validated)
            new_name = st.text_input(
                t.get("signup_fullname_label", "Full Name (Alphabetic letters & spaces only):"),
                placeholder=t.get("placeholder_name", "e.g. Ramesh Hegde / Ananya Rao"),
                key="signup_name_input"
            ).strip()

            # 10-Digit Mobile Contact (Strictly validated)
            new_phone = st.text_input(
                t.get("signup_mobile_label", "Mobile Contact (10-Digit Indian Mobile Number):"),
                placeholder=t.get("placeholder_phone", "e.g. 9845012345"),
                key="signup_phone_input"
            ).strip()

            new_email = st.text_input(
                t.get("signup_email_label", "Email Address (Optional):"),
                placeholder=t.get("placeholder_email", "e.g. user@hospital.org"),
                key="signup_email_input"
            ).strip()

            col_age, col_gen = st.columns(2)
            with col_age:
                new_age = st.number_input(t.get("signup_age_label", "Age:"), min_value=1, max_value=120, value=35, step=1, key="signup_age_input")
            with col_gen:
                gender_options = {
                    "Male": t.get("gender_male", "Male"),
                    "Female": t.get("gender_female", "Female"),
                    "Other": t.get("gender_other", "Other"),
                    "Prefer not to disclose": t.get("gender_undisclosed", "Prefer not to disclose")
                }
                new_gender = st.selectbox(
                    t.get("signup_gender_label", "Gender:"),
                    list(gender_options.keys()),
                    format_func=lambda k: gender_options[k],
                    key="signup_gender_input"
                )

            # ---------------- Patient Demographics & Health Profile ----------------
            st.markdown(f"<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>{t.get('signup_patient_sec', 'Patient Clinical Demographics')}</div>", unsafe_allow_html=True)
            blood_options = ["Unknown / Not Tested", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
            blood_labels = {
                "Unknown / Not Tested": t.get("blood_unknown", "Unknown / Not Tested"),
                "A+": "A+", "A-": "A-", "B+": "B+", "B-": "B-", "O+": "O+", "O-": "O-", "AB+": "AB+", "AB-": "AB-"
            }
            patient_blood_group = st.selectbox(
                t.get("signup_blood_group_label", "Blood Group:"),
                blood_options,
                format_func=lambda k: blood_labels.get(k, k),
                key="signup_blood_group"
            )

            col_emg1, col_emg2 = st.columns(2)
            with col_emg1:
                patient_emg_name = st.text_input(t.get("signup_emg_name_label", "Emergency Contact Person:"), placeholder=t.get("placeholder_emg_name", "e.g. Suresh Kumar (Brother)"), key="signup_emg_name").strip()
            with col_emg2:
                patient_emg_phone = st.text_input(t.get("signup_emg_phone_label", "Emergency Contact Mobile:"), placeholder="e.g. 9448199999", key="signup_emg_phone").strip()

            # ---------------- Location & Geolocation Section ----------------
            st.markdown(f"<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>{t.get('signup_addr_sec', 'Address & Location (GPS Auto-Detection or Manual)')}</div>", unsafe_allow_html=True)

            # GPS Auto-detect button
            col_gps_btn, col_gps_stat = st.columns([1.2, 2])
            with col_gps_btn:
                if st.button(t.get("signup_btn_gps", "📍 Auto-Detect Location (GPS)"), use_container_width=True, key="btn_detect_gps"):
                    loc = fetch_location_by_gps()
                    st.session_state["signup_loc_city"] = loc.get("city", "Mangaluru")
                    st.session_state["signup_loc_state"] = loc.get("state", "Karnataka")
                    st.session_state["signup_loc_pincode"] = loc.get("pincode", "575007")
                    st.session_state["signup_loc_coords"] = loc.get("gps_coordinates", "12.9187° N, 74.8598° E")
                    st.session_state["signup_gps_triggered"] = True
                    st.rerun()

            with col_gps_stat:
                if st.session_state.get("signup_gps_triggered", False):
                    st.markdown(f"<div style='font-size: 0.82rem; color: #166534; font-weight: 600; padding-top: 8px;'>{t.get('signup_gps_acquired', '✓ GPS Acquired:')} {st.session_state.get('signup_loc_city', '')}, {st.session_state.get('signup_loc_state', '')} ({st.session_state.get('signup_loc_coords', '')})</div>", unsafe_allow_html=True)
                else:
                    st.caption(t.get("signup_gps_caption", "Click button above to auto-fill address from GPS, or enter manually below."))

            address_street = st.text_input(
                t.get("signup_street_label", "Street Address / House No / Locality:"),
                placeholder=t.get("placeholder_street", "e.g. Main Hospital Road, Zone 2"),
                key="signup_addr_street"
            ).strip()

            col_c1, col_c2 = st.columns(2)
            with col_c1:
                address_city = st.text_input(
                    t.get("signup_city_label", "City / Town:"),
                    value=st.session_state.get("signup_loc_city", "Bantwal"),
                    key="signup_addr_city"
                ).strip()
            with col_c2:
                address_state = st.text_input(
                    t.get("signup_state_label", "State / Region:"),
                    value=st.session_state.get("signup_loc_state", "Karnataka"),
                    key="signup_addr_state"
                ).strip()

            col_pin, col_coord = st.columns(2)
            with col_pin:
                address_pincode = st.text_input(
                    t.get("signup_pincode_label", "Postal Pincode (6 Digits):"),
                    value=st.session_state.get("signup_loc_pincode", "574211"),
                    key="signup_addr_pincode"
                ).strip()
            with col_coord:
                gps_coords = st.text_input(
                    t.get("signup_coords_label", "GPS Coordinates (Lat/Long):"),
                    value=st.session_state.get("signup_loc_coords", "12.8913° N, 75.0347° E"),
                    key="signup_addr_coords"
                ).strip()

            # ---------------- Security Credentials ----------------
            st.markdown(f"<div style='font-size: 0.88rem; font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 4px;'>{t.get('signup_pw_sec', 'Account Password & Security')}</div>", unsafe_allow_html=True)
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                new_pw = st.text_input(
                    t.get("signup_pw_label", "Create Password (Min 6 chars):"),
                    type="password",
                    placeholder="Enter password",
                    key="signup_pw1"
                )
            with col_p2:
                confirm_pw = st.text_input(
                    t.get("signup_confirm_pw_label", "Confirm Password:"),
                    type="password",
                    placeholder="Re-enter password",
                    key="signup_pw2"
                )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if st.button(t.get("signup_btn_submit", "📝 Register & Create Secured Account"), type="primary", use_container_width=True, key="btn_signup_submit"):
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

                # 5. Role is strictly 'patient' for public self-registration
                role_code = "patient"
                doc_reg_val = None
                hosp_val = None
                doc_spec_val = None
                doc_exp_val = None

                # 6. Password Strength and Confirm Password Matching
                valid_pw, pw_err = validate_password(new_pw, confirm_pw)
                if not valid_pw:
                    st.error(f"⚠️ Password Security Error: {pw_err}")
                    st.stop()

                # ================= DATABASE INSERTION =================
                # Generate unique clean patient username
                clean_name_parts = [p.lower() for p in new_name.split() if p.isalpha()]
                first_name_str = clean_name_parts[0] if clean_name_parts else "user"
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

                    disp = f"{new_name} (+91 {cleaned_phone})"

                    st.session_state["user_id"] = disp
                    st.session_state["last_activity"] = time.time()

                    st.success(f"🎉 Account successfully created for {new_name}! Username: '{username_candidate}'. Redirecting...")
                    time.sleep(1.0)
                    st.rerun()


__all__ = ["render_auth_page"]
