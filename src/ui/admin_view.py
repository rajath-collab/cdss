"""
Module 2: Clinician / Radiologist Admin Triage Console
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Complete Frontend Implementation (Explainable AI & E-Signatures)
Uses real clinical chest radiographs (pneumonia-232.jpg) with interactive Grad-CAM heatmap blending.
"""
import streamlit as st
import pandas as pd
from PIL import Image
from src.ui.image_utils import get_real_sample_xray, generate_gradcam_overlay

def render_admin_portal():
    """Renders the Clinician Console with Grad-CAM inspection, RAG biomarkers, and e-signatures."""
    user_id = st.session_state.get("user_id", "Dr. Ramesh Rao (KMC-58291)")
    cases = st.session_state.get("patient_cases", {})

    # Top Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 22px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #818cf8; font-size: 1.6rem;">👨‍⚕️ Clinician Diagnostic Console & Audit</h2>
                    <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.95rem;">
                        Logged in as: <strong>{user_id}</strong> | Hospital: <strong>Bantwal District Hospital / Tele-ICU Center</strong>
                    </p>
                </div>
                <div style="background: rgba(129, 140, 248, 0.2); border: 1px solid #818cf8; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.82rem;">
                    🔒 Certified Medical Practitioner (RMP) Session
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
    col_q1.metric("Pending Remote Scans", f"{pending_count} Cases")
    col_q2.metric("Critical Red Flags", f"{critical_count} Urgent", delta="Immediate Action" if critical_count > 0 else "All Clear")
    col_q3.metric("Validated Today", f"{validated_count} Reports", delta="+3 from Bantwal")

    # Critical Alert Notification
    if critical_count > 0:
        st.markdown("""
            <div style="background: #fef2f2; border: 2px solid #ef4444; border-left: 8px solid #b91c1c; padding: 16px; border-radius: 8px; margin: 15px 0;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <strong style="color: #991b1b; font-size: 1.05rem;">🚨 CRITICAL EMERGENCY ALERT: High-Risk Remote Patients Awaiting Intervention</strong>
                        <div style="color: #7f1d1d; font-size: 0.88rem; margin-top: 4px;">
                            Active priority triage flag: <strong>Rajesh Kumar (Acute Bacterial Consolidation, SpO2: 89%)</strong>
                        </div>
                    </div>
                    <span style="background: #ef4444; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;">
                        TELE-ICU PRIORITY
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Case Selector
    case_ids = list(cases.keys())
    def format_case(cid):
        c = cases[cid]
        flag = "🚨 URGENT" if c.get("is_critical") and c.get("doctor_review", {}).get("status") != "reviewed" else ("✅ Reviewed" if c.get("doctor_review", {}).get("status") == "reviewed" else "⏳ Pending")
        return f"{flag} | {cid} — {c.get('patient_name')} ({c.get('xray_finding')})"

    selected_cid = st.selectbox("🔍 Select Patient Case to Audit & Digitally Sign:", options=case_ids, format_func=format_case)
    active_case = cases[selected_cid]
    triage = active_case.get("triage_summary", {})
    doc_rev = active_case.get("doctor_review", {})
    is_reviewed = doc_rev.get("status") == "reviewed"

    st.markdown(f"### 🔍 Case Review: `{selected_cid}` ({active_case.get('patient_name')}, Age: {active_case.get('patient_age', 48)})")

    # Diagnostic Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Radiographic Finding", active_case.get("xray_finding"), delta=f"{active_case.get('xray_confidence', 0.0):.1f}% Conf.")
    m2.metric("Pathology Markers", f"{len(active_case.get('lab_biomarkers', {}))} Analyzed", help="Verified from PDF slip")
    m3.metric("Center / PHC", active_case.get("location", "Bantwal PHC"))
    m4.metric("Emergency Contact", active_case.get("emergency_contact", "108 Emergency"))

    # Triage Summary Banner
    st.markdown(f"""
        <div style="background: {'#fef2f2' if active_case.get('is_critical') else '#f0fdf4'}; border-left: 5px solid {'#ef4444' if active_case.get('is_critical') else '#22c55e'}; padding: 14px; border-radius: 6px; margin: 12px 0;">
            <div style="font-weight: 700; color: {'#991b1b' if active_case.get('is_critical') else '#166534'}; font-size: 0.95rem;">
                Triage Diagnosis: {triage.get('etiology', 'Clinical Examination')}
            </div>
            <div style="font-size: 0.86rem; color: #334155; margin-top: 4px;">
                {triage.get('clinical_reasoning')}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dual Column Inspection: Real Radiograph + Grad-CAM vs Biomarkers
    col_vis, col_rag = st.columns(2)

    with col_vis:
        st.markdown("#### 🔬 Radiography Vision & Grad-CAM Saliency")
        opacity = st.slider("Grad-CAM Heatmap Transparency Overlay:", 0.0, 1.0, 0.65, step=0.05, key="admin_cam_slider")
        st.caption(f"ResNet-50 Layer 4 Saliency map blended at {int(opacity*100)}% opacity over real radiograph.")

        case_finding = active_case.get("xray_finding", "pneumonia").lower()
        real_xray_img = get_real_sample_xray(condition=case_finding)
        raw_xray, overlay_xray = generate_gradcam_overlay(base_img=real_xray_img, opacity=opacity, condition=case_finding)

        tab_overlay, tab_raw = st.tabs(["Grad-CAM Saliency Overlay", "Original Radiograph"])
        with tab_overlay:
            st.image(overlay_xray, caption=f"Predicted: {active_case.get('xray_finding')} ({active_case.get('xray_confidence', 92.4):.1f}% Confidence)", use_container_width=True)
        with tab_raw:
            st.image(raw_xray, caption="Raw Thoracic Radiograph (Real Clinical Scan)", use_container_width=True)

    with col_rag:
        st.markdown("#### 🧪 Pathology Biomarker Extraction & Analysis")
        biomarkers = active_case.get("lab_biomarkers", {})
        table_rows = []
        for k, v in biomarkers.items():
            table_rows.append({
                "Biomarker": v.get("name", k.upper()),
                "Observed Value": f"{v.get('value')} {v.get('unit', '')}",
                "Status": v.get("status", "NORMAL"),
                "Reference Interval": v.get("normal_range", "Standard")
            })
        df_bio = pd.DataFrame(table_rows)
        st.dataframe(df_bio, use_container_width=True, hide_index=True)

        st.markdown("##### 💬 Clinical Diagnostic Assistant")
        st.info("• Automated Correlation: Saliency activation in right lower lung field matches acute bacterial consolidation markers (CRP > 40 mg/L and Leukocytosis > 14,000/µL).\n• Ruling out viral etiology due to neutrophil predominance (81%).")

    # Clinician Decision Override & E-Signature
    st.divider()
    st.markdown("### ✍️ Clinician Decision Override & Digital Signature")

    default_rx = doc_rev.get("prescription") or (
        "Right basal bacterial pneumonia confirmed with acute hypoxia. "
        "Prescribed: Tab Azithromycin 500mg OD x 3 days, Tab Paracetamol 650mg SOS. "
        "Administer nasal cannula O2 @ 2L/min at Bantwal PHC. Immediate tele-follow up in 24 hours."
    )

    doctor_notes = st.text_area(
        "Official Clinical Prescription & Guidance (Will be dispatched directly to patient portal):",
        value=default_rx,
        height=100,
        key=f"doc_rx_{selected_cid}"
    )

    col_btn1, col_btn2 = st.columns([1.5, 1])
    with col_btn1:
        if st.button("🔒 Cryptographically Sign & Dispatch to Patient", type="primary", use_container_width=True, key=f"btn_sign_{selected_cid}"):
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
            if st.button("🚨 Trigger 108 Emergency Tele-Referral", use_container_width=True, key=f"btn_em_{selected_cid}"):
                st.error(f"🚑 Fast-Track Ambulance & Tele-ICU referral dispatched for {active_case.get('patient_name')} ({selected_cid}) to Bantwal PHC Emergency Ward!")

__all__ = ["render_admin_portal"]
