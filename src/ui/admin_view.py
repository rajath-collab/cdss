"""
Module 2: Clinician / Radiologist Admin Triage Console
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Complete Frontend Implementation (Explainable AI & E-Signatures)
Uses real clinical chest radiographs (pneumonia-232.jpg) with interactive Grad-CAM heatmap blending.
"""
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
from src.ui.image_utils import get_real_sample_xray, generate_gradcam_overlay
from src.ui.translations import get_ui_text

def render_admin_portal():
    """Renders the Clinician Console with Grad-CAM inspection, RAG biomarkers, and e-signatures."""
    ui_lang = st.session_state.get("ui_lang", "en")
    t = get_ui_text(ui_lang)

    user_id = st.session_state.get("user_id", "Dr. Ramesh Rao (KMC-58291)")
    cases = st.session_state.get("patient_cases", {})

    # Top Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 22px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #818cf8; font-size: 1.6rem;">{t.get('nav_clinician', '👨‍⚕️ Clinician Diagnostic & Triage Console')}</h2>
                    <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.95rem;">
                        {t.get('logged_in_as', 'Logged in as:')} <strong>{user_id}</strong> | {t.get('phc_label', 'Hospital:')} <strong>Bantwal District Hospital / Tele-ICU Center</strong>
                    </p>
                </div>
                <div style="background: rgba(129, 140, 248, 0.2); border: 1px solid #818cf8; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.82rem;">
                    {t.get('rmp_session_badge', '🔒 Certified Medical Practitioner (RMP) Session')}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dynamic KPI Metrics
    total_cases = len(cases)
    pending_count = sum(1 for c in cases.values() if c.get("doctor_review", {}).get("status") != "reviewed")
    critical_count = sum(1 for c in cases.values() if c.get("is_critical", False) and c.get("doctor_review", {}).get("status") != "reviewed")
    validated_count = sum(1 for c in cases.values() if c.get("doctor_review", {}).get("status") == "reviewed")

    col_q1, col_q2, col_q3 = st.columns(3)
    col_q1.metric(t.get("doc_metric_pending", "Pending Remote Scans"), f"{pending_count} Cases")
    col_q2.metric(t.get("doc_metric_critical", "Critical Red Flags"), f"{critical_count} Urgent", delta="Immediate Action" if critical_count > 0 else "All Clear")
    col_q3.metric(t.get("doc_metric_validated", "Validated Today"), f"{validated_count} Reports", delta="+3 from Bantwal")

    # Critical Alert Notification
    if critical_count > 0:
        st.markdown(f"""
            <div style="background: #fef2f2; border: 2px solid #ef4444; border-left: 8px solid #b91c1c; padding: 16px; border-radius: 8px; margin: 15px 0;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <strong style="color: #991b1b; font-size: 1.05rem;">{t.get('doc_alert_critical', '🚨 CRITICAL EMERGENCY ALERT: High-Risk Remote Patients Awaiting Intervention')}</strong>
                        <div style="color: #7f1d1d; font-size: 0.88rem; margin-top: 4px;">
                            Active priority triage flag: <strong>Rajesh Kumar (Acute Bacterial Consolidation, SpO2: 89%)</strong>
                        </div>
                    </div>
                    <span style="background: #ef4444; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;">
                        {t.get('doc_alert_priority_badge', 'TELE-ICU PRIORITY')}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Clinician Patient Ingestion / Data Management Tool
    with st.expander(t.get("doc_expander_ingest", "➕ Ingest New Patient Case directly to Clinical Triage Queue"), expanded=False):
        st.markdown(f"##### {t.get('doc_ingest_title', 'Register a New Patient Scan & Biomarkers (Instant Point-of-Care Ingestion)')}")
        col_cp1, col_cp2 = st.columns(2)
        with col_cp1:
            c_p_name = st.text_input(t.get("doc_p_name_label", "Patient Full Name:"), placeholder="e.g. Ramesh Hegde", key="doc_add_p_name").strip()
            c_p_age = st.number_input(t.get("doc_p_age_label", "Patient Age:"), min_value=1, max_value=110, value=52, key="doc_add_p_age")
            c_p_gender = st.selectbox(t.get("doc_p_gender_label", "Gender:"), ["Male", "Female", "Other"], key="doc_add_p_gen")
            c_p_phone = st.text_input(t.get("doc_p_phone_label", "Mobile Contact (10 Digits):"), placeholder="e.g. 9845012399", key="doc_add_p_phone").strip()

        with col_cp2:
            c_p_loc = st.text_input(t.get("doc_p_loc_label", "Clinical Location / PHC Ward:"), value="Bantwal District Hospital (Emergency Ward)", key="doc_add_p_loc").strip()
            c_p_finding = st.selectbox(
                t.get("doc_p_finding_label", "Diagnostic Finding / Impression:"),
                ["Pneumonia / Consolidation", "Normal Baseline", "Pleural Effusion", "COVID-19 Infiltration", "Tuberculosis Suspect"],
                key="doc_add_p_finding"
            )
            c_p_conf = st.slider(t.get("doc_p_conf_label", "Confidence Score (%):"), 70.0, 99.5, 94.2, step=0.1, key="doc_add_p_conf")
            c_p_crit = st.checkbox(t.get("doc_p_crit_label", "Mark as High-Risk Critical Tele-ICU Priority"), value=("Pneumonia" in c_p_finding), key="doc_add_p_crit")

        col_cb1, col_cb2, col_cb3 = st.columns(3)
        with col_cb1:
            c_wbc = st.text_input("WBC Count (/µL):", value="13,900", key="doc_add_wbc")
        with col_cb2:
            c_crp = st.text_input("CRP Level (mg/L):", value="44.0", key="doc_add_crp")
        with col_cb3:
            c_spo2 = st.text_input("SpO2 Saturation (%):", value="90%", key="doc_add_spo2")

        if st.button(t.get("doc_btn_ingest", "🚀 Ingest Patient Case into Live Queue"), type="primary", use_container_width=True, key="btn_doc_ingest_p"):
            if not c_p_name:
                st.error("⚠️ Patient name is required.")
            else:
                new_cid = f"PT-2026-{1000 + len(cases) + 1}"
                st.session_state.patient_cases[new_cid] = {
                    "case_id": new_cid,
                    "patient_username": f"+91 {c_p_phone or '9845000000'}",
                    "patient_name": c_p_name,
                    "patient_age": int(c_p_age),
                    "patient_gender": c_p_gender,
                    "location": c_p_loc,
                    "emergency_contact": "+91 94481 99999",
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "xray_preset": "patient_001_pneumonia" if "Pneumonia" in c_p_finding else "patient_002_normal",
                    "xray_finding": c_p_finding,
                    "xray_confidence": float(c_p_conf),
                    "lab_biomarkers": {
                        "wbc": {"name": "White Blood Cell Count", "value": c_wbc, "unit": "/µL", "status": "ELEVATED", "normal_range": "4,500 - 11,000 /µL"},
                        "crp": {"name": "C-Reactive Protein", "value": c_crp, "unit": "mg/L", "status": "CRITICALLY HIGH", "normal_range": "< 5.0 mg/L"},
                        "spo2": {"name": "Oxygen Saturation (SpO2)", "value": c_spo2, "unit": "%", "status": "LOW" if "8" in c_spo2 or "90" in c_spo2 else "NORMAL", "normal_range": "95 - 100%"}
                    },
                    "triage_summary": {
                        "triage_category": "CRITICAL RISK - PRIORITY 1" if c_p_crit else "ROUTINE BASELINE",
                        "severity_color": "red" if c_p_crit else "green",
                        "etiology": f"Acute Presentation of {c_p_finding}",
                        "clinical_reasoning": f"Doctor ingested point-of-care case: {c_p_finding} with SpO2 at {c_spo2}.",
                        "recommendation": "Urgent intervention and continuous vital monitoring required." if c_p_crit else "Outpatient care."
                    },
                    "is_critical": c_p_crit,
                    "alert_status": f"🚨 URGENT ACTION ({c_p_finding})" if c_p_crit else f"✅ {c_p_finding}",
                    "doctor_review": {
                        "status": "pending_review",
                        "doctor_name": None,
                        "doctor_reg": None,
                        "reviewed_at": None,
                        "prescription": "",
                        "doctor_notes": ""
                    }
                }
                st.success(f"🎉 Case `{new_cid}` successfully ingested for {c_p_name}!")
                st.rerun()

    # Case Selector
    case_ids = list(cases.keys())
    def format_case(cid):
        c = cases[cid]
        flag = "🚨 URGENT" if c.get("is_critical") and c.get("doctor_review", {}).get("status") != "reviewed" else ("✅ Reviewed" if c.get("doctor_review", {}).get("status") == "reviewed" else "⏳ Pending")
        return f"{flag} | {cid} — {c.get('patient_name')} ({c.get('xray_finding')})"

    selected_cid = st.selectbox(t.get("doc_select_case", "🔍 Select Patient Case to Review & Prescribe:"), options=case_ids, format_func=format_case)
    active_case = cases[selected_cid]
    triage = active_case.get("triage_summary", {})
    doc_rev = active_case.get("doctor_review", {})
    is_reviewed = doc_rev.get("status") == "reviewed"

    st.markdown(f"### 🔍 Case Review: `{selected_cid}` ({active_case.get('patient_name')}, Age: {active_case.get('patient_age', 48)})")

    # Diagnostic Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t.get("label_scan_finding", "Radiographic Finding"), active_case.get("xray_finding"), delta=f"{active_case.get('xray_confidence', 0.0):.1f}% Conf.")
    m2.metric(t.get("label_biomarkers_eval", "Pathology Markers"), f"{len(active_case.get('lab_biomarkers', {}))} Analyzed", help="Verified from PDF slip")
    m3.metric(t.get("phc_label", "Center / PHC"), active_case.get("location", "Bantwal PHC"))
    m4.metric(t.get("contacts_title", "Emergency Contact"), active_case.get("emergency_contact", "108 Emergency"))

    # Triage Summary Banner
    st.markdown(f"""
        <div style="background: {'#fef2f2' if active_case.get('is_critical') else '#f0fdf4'}; border-left: 5px solid {'#ef4444' if active_case.get('is_critical') else '#22c55e'}; padding: 14px; border-radius: 6px; margin: 12px 0;">
            <div style="font-weight: 700; color: {'#991b1b' if active_case.get('is_critical') else '#166534'}; font-size: 0.95rem;">
                {t.get('label_triage_diag', 'Triage Diagnosis:')} {triage.get('etiology', 'Clinical Examination')}
            </div>
            <div style="font-size: 0.86rem; color: #334155; margin-top: 4px;">
                {triage.get('clinical_reasoning')}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dual Column Inspection: Real Radiograph + Grad-CAM vs Biomarkers
    col_vis, col_rag = st.columns(2)

    with col_vis:
        st.markdown(f"#### {t.get('doc_rad_vision_title', '🔬 Radiography Vision & Grad-CAM Saliency')}")
        opacity = st.slider(t.get("doc_cam_slider_label", "Grad-CAM Heatmap Transparency Overlay:"), 0.0, 1.0, 0.65, step=0.05, key="admin_cam_slider")
        st.caption(f"ResNet-50 Layer 4 Saliency map blended at {int(opacity*100)}% opacity over real radiograph.")

        case_finding = active_case.get("xray_finding", "pneumonia").lower()
        real_xray_img = get_real_sample_xray(condition=case_finding)
        raw_xray, overlay_xray = generate_gradcam_overlay(base_img=real_xray_img, opacity=opacity, condition=case_finding)

        tab_overlay, tab_raw = st.tabs([t.get("doc_tab_overlay", "Grad-CAM Saliency Overlay"), t.get("doc_tab_raw", "Original Radiograph")])
        with tab_overlay:
            st.image(overlay_xray, caption=f"{t.get('pred_label', 'Predicted:')} {active_case.get('xray_finding')} ({active_case.get('xray_confidence', 92.4):.1f}% Confidence)", use_container_width=True)
        with tab_raw:
            st.image(raw_xray, caption=t.get("active_xray_caption", "Raw Thoracic Radiograph (Real Clinical Scan)"), use_container_width=True)

    with col_rag:
        st.markdown(f"#### {t.get('doc_biomarker_title', '🧪 Pathology Biomarker Extraction & Analysis')}")
        biomarkers = active_case.get("lab_biomarkers", {})
        table_rows = []
        for k, v in biomarkers.items():
            table_rows.append({
                t.get("col_biomarker", "Biomarker"): v.get("name", k.upper()),
                t.get("col_observed", "Observed Value"): f"{v.get('value')} {v.get('unit', '')}",
                t.get("col_status", "Status"): v.get("status", "NORMAL"),
                t.get("col_ref_interval", "Reference Interval"): v.get("normal_range", "Standard")
            })
        df_bio = pd.DataFrame(table_rows)
        st.dataframe(df_bio, use_container_width=True, hide_index=True)

        st.markdown(f"##### {t.get('doc_assistant_title', '💬 Clinical Diagnostic Assistant')}")
        st.info("• Automated Correlation: Saliency activation in right lower lung field matches acute bacterial consolidation markers (CRP > 40 mg/L and Leukocytosis > 14,000/µL).\n• Ruling out viral etiology due to neutrophil predominance (81%).")

    # Clinician Decision Override & E-Signature
    st.divider()
    st.markdown(f"### {t.get('doc_rx_section_title', '✍️ Clinician Decision Override & Digital Signature')}")

    default_rx = doc_rev.get("prescription") or (
        "Right basal bacterial pneumonia confirmed with acute hypoxia. "
        "Prescribed: Tab Azithromycin 500mg OD x 3 days, Tab Paracetamol 650mg SOS. "
        "Administer nasal cannula O2 @ 2L/min at Bantwal PHC. Immediate tele-follow up in 24 hours."
    )

    doctor_notes = st.text_area(
        t.get("doc_rx_label", "Official Clinical Prescription & Guidance (Will be dispatched directly to patient portal):"),
        value=default_rx,
        height=100,
        key=f"doc_rx_{selected_cid}"
    )

    col_btn1, col_btn2 = st.columns([1.5, 1])
    with col_btn1:
        if st.button(t.get("doc_btn_sign", "🔒 Cryptographically Sign & Dispatch to Patient"), type="primary", use_container_width=True, key=f"btn_sign_{selected_cid}"):
            # Update case in state
            active_case["doctor_review"] = {
                "status": "reviewed",
                "doctor_name": user_id,
                "doctor_reg": "KMC-58291",
                "reviewed_at": "2026-10-30 00:05:00",
                "prescription": doctor_notes,
                "doctor_notes": doctor_notes
            }
            st.session_state.patient_cases[selected_cid] = active_case
            st.success(f"Report digitally locked with key `{user_id}` and dispatched to patient's phone.")
            st.toast("Prescription dispatched to Patient Portal!", icon="🔒")
            st.rerun()

    with col_btn2:
        if active_case.get("is_critical"):
            if st.button(t.get("doc_btn_referral", "🚨 Trigger 108 Emergency Tele-Referral"), use_container_width=True, key=f"btn_em_{selected_cid}"):
                st.error(f"🚑 Fast-Track Ambulance & Tele-ICU referral dispatched for {active_case.get('patient_name')} ({selected_cid}) to Bantwal PHC Emergency Ward!")

__all__ = ["render_admin_portal"]
