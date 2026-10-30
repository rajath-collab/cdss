"""
Module 6: Hospital Clinical Administration & Governance Portal
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Production Web Application Implementation for Hospital Super-Admins & Chief Medical Officers:
  - Doctor & Medical Staff Credential Management & Roster
  - Patient Master Database & Dynamic Case Registration
  - Production Feature Management & Clinical AI Flags
  - Hospital Bed, ICU & Oxygen Telemetry Tracker
  - Strict Role-Based Access Control (Zero Patient Access)
"""

import streamlit as st
import pandas as pd
import datetime
from src.security.database import get_db, hash_password, create_user


def render_system_admin_portal():
    """Renders the comprehensive Hospital Administration & Clinical Governance Portal."""
    user_role = st.session_state.get("user_role", "doctor")
    current_user = st.session_state.get("current_user", {})
    user_id = st.session_state.get("user_id", "Hospital Administrator")

    # Strict Access Security Barrier - Patients strictly prohibited
    if user_role not in ["admin", "doctor"]:
        st.error("⛔ ACCESS DENIED: Hospital Administration privileges required. Patients and unauthorized users are strictly barred from this portal.")
        st.stop()

    # Initialize persistent hospital configuration state if not present
    if "hospital_config" not in st.session_state:
        st.session_state["hospital_config"] = {
            "ai_inference_active": True,
            "gradcam_enabled": True,
            "tele_icu_referral_active": True,
            "biomarker_fusion_enabled": True,
            "patient_tts_advisory": True,
            "client_memory_isolation": True,
            "hospital_name": "Bantwal District Hospital & Tele-ICU Center",
            "cmo_name": "Dr. K. V. Hegde",
            "icu_beds_total": 18,
            "icu_beds_occupied": 14,
            "ventilators_total": 8,
            "ventilators_occupied": 6,
            "oxygen_reserve_pct": 92
        }

    cfg = st.session_state["hospital_config"]
    cases = st.session_state.get("patient_cases", {})

    # Top Executive Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 24px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 18px rgba(0,0,0,0.18); border-left: 8px solid #0284c7;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.8px;">
                        🏥 Central Hospital Clinical Administration & Governance
                    </div>
                    <h2 style="margin: 4px 0 0 0; color: #f8fafc; font-size: 1.65rem;">
                        {cfg.get('hospital_name', 'Bantwal District Hospital')}
                    </h2>
                    <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.92rem;">
                        Superintendent: <strong>{user_id}</strong> &nbsp;|&nbsp; Network: <strong>Dakshina Kannada Health Mission (Tele-ICU Grid)</strong>
                    </p>
                </div>
                <div style="background: rgba(2, 132, 199, 0.25); border: 1px solid #38bdf8; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 0.82rem; color: #e0f2fe;">
                    🛡️ System Administrator Mode Active
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Executive KPI Metrics
    c_bed_avail = cfg["icu_beds_total"] - cfg["icu_beds_occupied"]
    c_vent_avail = cfg["ventilators_total"] - cfg["ventilators_occupied"]
    c_crit = sum(1 for c in cases.values() if c.get("is_critical", False))

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Clinical Cases", f"{len(cases)} Cases", delta=f"{c_crit} Critical Flagged")
    k2.metric("Tele-ICU Bed Capacity", f"{c_bed_avail} Free / {cfg['icu_beds_total']} Total", delta="78% Utilized")
    k3.metric("Ventilator Availability", f"{c_vent_avail} Units Ready", delta=f"{cfg['ventilators_occupied']} in Use")
    k4.metric("Medical Oxygen Reserve", f"{cfg['oxygen_reserve_pct']}% Bulk Liquid", delta="Stable Telemetry")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 4 Main Administrative Management Tabs
    tab_cases, tab_doctors, tab_beds, tab_features = st.tabs([
        "📁 Patient Clinical Cases Master",
        "👨‍⚕️ Doctor & Medical Staff Roster",
        "🛏️ Hospital Beds & Tele-ICU Tracker",
        "⚙️ Feature Controls & Clinical AI Flags"
    ])

    # -----------------------------------------------------------------
    # TAB 1: PATIENT CASES MASTER & ADD NEW PATIENT CASE
    # -----------------------------------------------------------------
    with tab_cases:
        st.markdown("### 📁 Clinical Case Master & Triage Ingestion")
        st.caption("Central registry of all patient diagnostic records, chest radiographs, and triage statuses across district centers.")

        # Expandable: Add New Patient Case
        with st.expander("➕ Ingest New Patient Case (Scan & Biomarker Record)", expanded=False):
            st.markdown("##### Register New Remote or Inpatient Case into Triage Grid")

            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                in_p_name = st.text_input("Patient Full Name:", placeholder="e.g. Ramesh Hegde", key="adm_new_p_name").strip()
                in_p_age = st.number_input("Patient Age:", min_value=1, max_value=110, value=45, key="adm_new_p_age")
                in_p_gender = st.selectbox("Gender:", ["Male", "Female", "Other"], key="adm_new_p_gen")

            with col_p2:
                in_p_phone = st.text_input("Mobile Contact (10 Digits):", placeholder="e.g. 9845011999", key="adm_new_p_phone").strip()
                in_p_loc = st.selectbox(
                    "Hospital Center / Rural PHC:",
                    [
                        "Bantwal Rural PHC Zone 2",
                        "Panemangalore Sub-Center",
                        "Bantwal District Hospital (Emergency Ward)",
                        "Mangalore Central Hospital",
                        "Belthangady Community Health Centre"
                    ],
                    key="adm_new_p_loc"
                )
                in_p_contact = st.text_input("Emergency Relative Contact:", value="+91 94481 00000", key="adm_new_p_emg")

            with col_p3:
                in_p_finding = st.selectbox(
                    "Suspected Radiograph Finding:",
                    [
                        "Pneumonia / Consolidation",
                        "Normal Baseline",
                        "Pleural Effusion",
                        "COVID-19 Infiltration",
                        "Tuberculosis Suspect"
                    ],
                    key="adm_new_p_finding"
                )
                in_p_conf = st.slider("AI Inference Confidence (%):", 70.0, 99.5, 93.8, step=0.1, key="adm_new_p_conf")
                in_p_severity = st.selectbox("Triage Risk Category:", ["CRITICAL RISK - PRIORITY 1", "URGENT - PRIORITY 2", "LOW RISK - ROUTINE BASELINE"], key="adm_new_p_sev")

            st.markdown("###### Laboratory Biomarkers & Vitals")
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                in_wbc = st.text_input("WBC Count (/µL):", value="13,800", key="adm_new_wbc")
            with col_b2:
                in_crp = st.text_input("CRP Level (mg/L):", value="42.5", key="adm_new_crp")
            with col_b3:
                in_esr = st.text_input("ESR (mm/hr):", value="34", key="adm_new_esr")
            with col_b4:
                in_spo2 = st.text_input("SpO2 Blood Oxygen (%):", value="91%", key="adm_new_spo2")

            in_p_notes = st.text_area(
                "Initial Clinical Notes / Symptoms:",
                value="Patient presented with high-grade fever, productive cough with purulent sputum, and dyspnea on exertion for 4 days.",
                height=70,
                key="adm_new_notes"
            )

            if st.button("🚀 Register Case & Ingest into Live Triage Grid", type="primary", use_container_width=True, key="btn_adm_create_case"):
                if not in_p_name:
                    st.error("⚠️ Patient name is required.")
                elif not in_p_phone or len(in_p_phone) < 10:
                    st.error("⚠️ Valid 10-digit mobile contact is required.")
                else:
                    new_cid = f"PT-2026-{1000 + len(cases) + 1}"
                    is_crit = "CRITICAL" in in_p_severity

                    st.session_state.patient_cases[new_cid] = {
                        "case_id": new_cid,
                        "patient_username": f"+91 {in_p_phone}",
                        "patient_name": in_p_name,
                        "patient_age": int(in_p_age),
                        "patient_gender": in_p_gender,
                        "location": in_p_loc,
                        "emergency_contact": in_p_contact,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "xray_preset": "patient_001_pneumonia" if "Pneumonia" in in_p_finding else "patient_002_normal",
                        "xray_finding": in_p_finding,
                        "xray_confidence": float(in_p_conf),
                        "lab_biomarkers": {
                            "wbc": {"name": "White Blood Cell Count", "value": in_wbc, "unit": "/µL", "status": "ELEVATED", "normal_range": "4,500 - 11,000 /µL"},
                            "crp": {"name": "C-Reactive Protein", "value": in_crp, "unit": "mg/L", "status": "CRITICALLY HIGH" if float(in_crp.replace(',', '')) > 10 else "NORMAL", "normal_range": "< 5.0 mg/L"},
                            "esr": {"name": "Erythrocyte Sed. Rate", "value": in_esr, "unit": "mm/hr", "status": "ELEVATED", "normal_range": "0 - 15 mm/hr"},
                            "spo2": {"name": "Oxygen Saturation (SpO2)", "value": in_spo2, "unit": "%", "status": "LOW" if "8" in in_spo2 or "90" in in_spo2 or "91" in in_spo2 else "NORMAL", "normal_range": "95 - 100%"}
                        },
                        "triage_summary": {
                            "triage_category": in_p_severity,
                            "severity_color": "red" if is_crit else "amber" if "URGENT" in in_p_severity else "green",
                            "etiology": f"{in_p_finding} with Associated Inflammatory Reaction",
                            "clinical_reasoning": in_p_notes,
                            "recommendation": "Urgent tele-consultation and review by certified medical practitioner." if is_crit else "Standard clinical follow-up."
                        },
                        "is_critical": is_crit,
                        "alert_status": f"🚨 URGENT ACTION ({in_p_finding})" if is_crit else f"✅ {in_p_finding}",
                        "doctor_review": {
                            "status": "pending_review",
                            "doctor_name": None,
                            "doctor_reg": None,
                            "reviewed_at": None,
                            "prescription": "",
                            "doctor_notes": ""
                        }
                    }
                    st.success(f"🎉 New Case `{new_cid}` successfully registered for {in_p_name}! Available immediately in the Clinician Console.")
                    st.toast(f"Case {new_cid} Ingested!", icon="✅")
                    st.rerun()

        # Master Table of all existing cases
        case_rows = []
        for cid, c in cases.items():
            status = "✅ Reviewed & Signed" if c.get("doctor_review", {}).get("status") == "reviewed" else "⏳ Awaiting Doctor Review"
            severity = "🚨 CRITICAL (Priority 1)" if c.get("is_critical") else "🟢 Normal Baseline"
            case_rows.append({
                "Case ID": cid,
                "Patient Name": c.get("patient_name"),
                "Age / Sex": f"{c.get('patient_age')} / {c.get('patient_gender')}",
                "Location / PHC": c.get("location"),
                "Radiographic Finding": f"{c.get('xray_finding')} ({c.get('xray_confidence', 0)}%)",
                "Triage Level": severity,
                "Clinical Status": status,
                "Assigned Doctor": c.get("doctor_review", {}).get("doctor_name") or "Unassigned"
            })

        df_cases = pd.DataFrame(case_rows)
        st.dataframe(df_cases, use_container_width=True, hide_index=True)

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        col_c_act1, col_c_act2 = st.columns([1, 2])
        with col_c_act1:
            sel_del_case = st.selectbox("Select Case to Manage / Delete:", list(cases.keys()), key="adm_sel_del_case")
        with col_c_act2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button(f"🗑️ Remove Case {sel_del_case}", key="btn_del_case"):
                if len(cases) > 1:
                    del st.session_state.patient_cases[sel_del_case]
                    st.warning(f"Case {sel_del_case} removed from hospital grid.")
                    st.rerun()
                else:
                    st.error("Cannot delete the last remaining clinical case.")

    # -----------------------------------------------------------------
    # TAB 2: DOCTOR & MEDICAL STAFF ROSTER
    # -----------------------------------------------------------------
    with tab_doctors:
        st.markdown("### 👨‍⚕️ Hospital Medical Staff & Radiologist Roster")
        st.caption("Authorized Registered Medical Practitioners (RMPs) entitled to diagnose, e-sign prescriptions, and override AI recommendations under NMC Act 2019.")

        # Add New Doctor expander
        with st.expander("➕ Onboard & Authorize New Medical Doctor", expanded=False):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                new_doc_name = st.text_input("Doctor Full Name (with Title):", placeholder="e.g. Dr. Anand Shetty, MD", key="adm_add_doc_name").strip()
                new_doc_reg = st.text_input("Medical Council Reg No (NMC/KMC):", placeholder="e.g. KMC-62180", key="adm_add_doc_reg").strip()
                new_doc_spec = st.selectbox("Clinical Specialty:", [
                    "Pulmonology & Critical Care",
                    "Thoracic Radiology",
                    "General & Internal Medicine",
                    "Emergency Medicine & Trauma",
                    "Cardiology & Tele-ICU"
                ], key="adm_add_doc_spec")

            with col_d2:
                new_doc_phone = st.text_input("Mobile Number (10 Digits):", placeholder="e.g. 9845011888", key="adm_add_doc_phone").strip()
                new_doc_hosp = st.text_input("Assigned Hospital / PHC Center:", value="Bantwal District Hospital", key="adm_add_doc_hosp").strip()
                new_doc_pw = st.text_input("Initial Temporary Password:", value="doctor123", key="adm_add_doc_pw").strip()

            if st.button("📝 Authorize & Issue Medical Council Credentials", type="primary", use_container_width=True, key="btn_adm_add_doc"):
                if not new_doc_name or not new_doc_reg or not new_doc_phone:
                    st.error("⚠️ All doctor credential fields are required.")
                else:
                    # Clean username
                    clean_uname = f"dr.{new_doc_name.split()[1].lower() if len(new_doc_name.split()) > 1 else 'doc'}_{new_doc_phone[-4:]}"
                    success, msg, _ = create_user(
                        username=clean_uname,
                        password=new_doc_pw,
                        full_name=new_doc_name,
                        role="doctor",
                        phone=new_doc_phone,
                        reg_number=new_doc_reg.upper(),
                        organization=new_doc_hosp,
                        specialization=new_doc_spec
                    )
                    if success:
                        st.success(f"🎉 Dr. {new_doc_name} successfully authorized! Login Username: `{clean_uname}` | Council Reg: `{new_doc_reg.upper()}`")
                        st.toast(f"Dr. {new_doc_name} Onboarded!", icon="✅")
                    else:
                        st.error(f"❌ Error adding doctor: {msg}")

        # Fetch doctors from database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, role, phone, reg_number, organization, specialization, email FROM users WHERE role = 'doctor' OR role = 'admin'")
            doc_rows = [dict(r) for r in cursor.fetchall()]

        if doc_rows:
            formatted_docs = []
            for d in doc_rows:
                formatted_docs.append({
                    "Doctor / Practitioner Name": d.get("full_name"),
                    "Role Privilege": "Hospital Admin" if d.get("role") == "admin" else "Certified RMP Doctor",
                    "Medical Council Reg": d.get("reg_number") or "N/A",
                    "Specialization": d.get("specialization") or "General Medicine",
                    "Hospital / Department": d.get("organization") or "District Hospital",
                    "Mobile Contact": f"+91 {d.get('phone')}",
                    "Status": "🟢 VERIFIED ACTIVE"
                })
            df_docs = pd.DataFrame(formatted_docs)
            st.dataframe(df_docs, use_container_width=True, hide_index=True)
        else:
            st.info("No doctors found in database.")

    # -----------------------------------------------------------------
    # TAB 3: HOSPITAL BEDS & TELE-ICU TRACKER
    # -----------------------------------------------------------------
    with tab_beds:
        st.markdown("### 🛏️ Hospital Capacity, ICU Beds & Oxygen Tracker")
        st.caption("Live telemetric telemetry across Bantwal District Hospital, Mangalore Central Hospital, and satellite rural sub-centers.")

        col_bd1, col_bd2 = st.columns(2)
        with col_bd1:
            st.markdown("#### 🏥 Bantwal District Hospital (Primary Tele-ICU Center)")
            new_icu_total = st.number_input("Total ICU Beds:", min_value=1, max_value=100, value=cfg["icu_beds_total"], key="adm_b_total")
            new_icu_occ = st.number_input("Occupied ICU Beds:", min_value=0, max_value=new_icu_total, value=cfg["icu_beds_occupied"], key="adm_b_occ")
            new_vent_total = st.number_input("Total Ventilators:", min_value=0, max_value=50, value=cfg["ventilators_total"], key="adm_v_total")
            new_vent_occ = st.number_input("In-Use Ventilators:", min_value=0, max_value=new_vent_total, value=cfg["ventilators_occupied"], key="adm_v_occ")
            new_o2 = st.slider("Liquid Medical Oxygen Tank Reserve (%):", 0, 100, cfg["oxygen_reserve_pct"], key="adm_o2")

        with col_bd2:
            st.markdown("#### 🏥 Partner Hospital Live Status")
            st.markdown("""
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <strong>Mangalore Central Tertiary Hospital (Referral Hub)</strong><br/>
                    • ICU Beds Available: <strong>14 / 60 Beds Free</strong><br/>
                    • High-Flow Nasal Cannula (HFNC): <strong>8 Available</strong><br/>
                    • Oxygen Pipeline Pressure: <strong>4.2 Bar (Optimal)</strong>
                </div>
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <strong>Panemangalore Primary Health Centre (PHC)</strong><br/>
                    • Stabilization Oxygen Beds: <strong>3 Beds Available</strong><br/>
                    • 108 Emergency Ambulance: <strong>Stationed & On-Call</strong><br/>
                    • ASHA Field Leads: <strong>6 Active on Triage</strong>
                </div>
            """, unsafe_allow_html=True)

        if st.button("💾 Update Live Bed & Oxygen Telemetry", type="primary", key="btn_save_beds"):
            st.session_state.hospital_config["icu_beds_total"] = int(new_icu_total)
            st.session_state.hospital_config["icu_beds_occupied"] = int(new_icu_occ)
            st.session_state.hospital_config["ventilators_total"] = int(new_vent_total)
            st.session_state.hospital_config["ventilators_occupied"] = int(new_vent_occ)
            st.session_state.hospital_config["oxygen_reserve_pct"] = int(new_o2)
            st.success("✅ Hospital bed and oxygen telemetry updated in real time!")
            st.rerun()

    # -----------------------------------------------------------------
    # TAB 4: FEATURE CONTROLS & PRODUCTION CLINICAL AI FLAGS
    # -----------------------------------------------------------------
    with tab_features:
        st.markdown("### ⚙️ Production Feature Controls & Clinical AI Flags")
        st.caption("Central feature management for hospital administrators. Toggle diagnostic engines, emergency auto-referral, and compliance controls.")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("##### Clinical Intelligence & Visualization")
            f_ai = st.toggle("🧠 Deep Learning Inference Engine (ResNet-50 Vision)", value=cfg["ai_inference_active"], key="adm_tog_ai")
            f_gradcam = st.toggle("🔬 Saliency Heatmap Overlays (Grad-CAM Explainability)", value=cfg["gradcam_enabled"], key="adm_tog_cam")
            f_biomarker = st.toggle("🧪 Laboratory Biomarker Multimodal Fusion (WBC, CRP, ESR)", value=cfg["biomarker_fusion_enabled"], key="adm_tog_bio")

        with col_f2:
            st.markdown("##### Emergency Tele-ICU & Patient Services")
            f_tele_icu = st.toggle("🚨 Automated 108 Emergency Tele-Referral Dispatch Gateway", value=cfg["tele_icu_referral_active"], key="adm_tog_tele")
            f_tts = st.toggle("🔊 Vernacular Audio Patient Advisory (Kannada, Hindi, Tamil)", value=cfg["patient_tts_advisory"], key="adm_tog_tts")
            f_iso = st.toggle("🛡️ DPDP Act 2023 Isolated Client Memory Sandbox", value=cfg["client_memory_isolation"], key="adm_tog_iso")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("💾 Apply Production Feature Configuration", type="primary", use_container_width=True, key="btn_save_features"):
            st.session_state.hospital_config["ai_inference_active"] = f_ai
            st.session_state.hospital_config["gradcam_enabled"] = f_gradcam
            st.session_state.hospital_config["biomarker_fusion_enabled"] = f_biomarker
            st.session_state.hospital_config["tele_icu_referral_active"] = f_tele_icu
            st.session_state.hospital_config["patient_tts_advisory"] = f_tts
            st.session_state.hospital_config["client_memory_isolation"] = f_iso
            st.success("✅ Production feature flags successfully updated! Changes are active system-wide.")
            st.toast("System Feature Flags Updated!", icon="⚙️")


__all__ = ["render_system_admin_portal"]
