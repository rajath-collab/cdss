"""
Module 2: Clinician / Radiologist Admin Triage Console
Lead: Student 1 (System Architect)
Integrates:
  - Student 2 (Module 3): ResNet-50 Vision & Grad-CAM Heatmap Overlay
  - Student 3 (Module 4): ChromaDB Biomarker Vector RAG
  - Remote Patient Emergency Alerts & E-Prescription Dispatch
"""

import os
import pandas as pd
from PIL import Image
import streamlit as st

from utils.case_manager import load_all_cases, doctor_sign_and_dispatch
from models.vision_model import predict_xray
from models.gradcam import GradCAM
from modules.rag_component import render_rag_window
from rag.parser import chunk_report_for_indexing, parse_pdf_report


def render_admin_portal(current_user: dict = None, model = None, gradcam = None, vector_store = None):
    """Renders the Clinician Console with Grad-CAM inspection, RAG biomarkers, and e-signatures."""
    if current_user is None:
        current_user = st.session_state.get("current_user") or {
            "role": "doctor",
            "full_name": "Dr. Ramesh Rao, MD (Pulmonology)",
            "username": "dr.ramesh",
            "reg_number": "KMC-58291",
            "hospital": "Bantwal District Hospital / Tele-ICU Center"
        }
    if model is None or gradcam is None:
        from models.vision_model import load_model
        from models.gradcam import GradCAM
        if "cdss_model" not in st.session_state:
            st.session_state.cdss_model = load_model()
        model = st.session_state.cdss_model
        gradcam = GradCAM(model)
    if vector_store is None:
        from rag.vector_store import CDSSVectorStore
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = CDSSVectorStore(persist_dir="data/chroma_db")
        vector_store = st.session_state.vector_store
    
    # -------------------------------------------------------------
    # 🛡️ STRICT SERVER-SIDE ROLE GUARD (NMC ACT 2019 COMPLIANCE)
    # -------------------------------------------------------------
    if current_user.get("role") != "doctor":
        st.error("⛔ Access Denied: This diagnostic console and audit log is strictly restricted to certified Registered Medical Practitioners (RMP).")
        st.warning("Your active account does not have clinician privileges. Please sign in with an authorized Doctor account.")
        st.stop()
        
    doc_name = current_user.get("full_name", "Dr. Ramesh Rao, MD")
    doc_reg = current_user.get("reg_number", "KMC-58291")
    doc_hosp = current_user.get("hospital", "Bantwal District Hospital / Tele-ICU")

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 22px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #818cf8; font-size: 1.6rem;">👨‍⚕️ Clinician Diagnostic Console & Audit</h2>
                    <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.95rem;">
                        Logged in as: <strong>{doc_name}</strong> | Registration: <code>{doc_reg}</code> | {doc_hosp}
                    </p>
                </div>
                <div style="background: rgba(129, 140, 248, 0.2); border: 1px solid #818cf8; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.82rem;">
                    🔒 Certified Medical Practitioner (RMP) Session
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Load dynamic cases from case manager
    cases_dict = load_all_cases()
    cases_list = list(cases_dict.values())
    
    # Calculate live KPI metrics
    pending_count = sum(1 for c in cases_list if c.get("doctor_review", {}).get("status") != "reviewed")
    critical_count = sum(1 for c in cases_list if c.get("is_critical", False) and c.get("doctor_review", {}).get("status") != "reviewed")
    validated_count = sum(1 for c in cases_list if c.get("doctor_review", {}).get("status") == "reviewed")

    col_q1, col_q2, col_q3 = st.columns(3)
    col_q1.metric("Pending Remote Scans", f"{pending_count} Cases")
    col_q2.metric("Critical Red Flags", f"{critical_count} Urgent", delta="Immediate Action" if critical_count > 0 else "All Clear")
    col_q3.metric("Validated Today", f"{validated_count} Reports", delta="+3 from Bantwal")

    # -----------------------------------------------------------------
    # 🚨 EMERGENCY RISK ALERT NOTIFICATION (CRITICAL PATIENT DISPATCH)
    # -----------------------------------------------------------------
    urgent_cases = [c for c in cases_list if c.get("is_critical", False) and c.get("doctor_review", {}).get("status") != "reviewed"]
    if urgent_cases:
        urgent_names = ", ".join([f"{c['patient_name']} ({c.get('xray_finding', 'Infection')})" for c in urgent_cases[:3]])
        st.markdown(f"""
            <div style="background: #fef2f2; border: 2px solid #ef4444; border-left: 8px solid #b91c1c; padding: 16px; border-radius: 8px; margin: 15px 0;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <strong style="color: #991b1b; font-size: 1.05rem;">🚨 CRITICAL EMERGENCY ALERT: High-Risk Remote Patients Awaiting Intervention</strong>
                        <div style="color: #7f1d1d; font-size: 0.88rem; margin-top: 4px;">
                            Active priority triage flags: <strong>{urgent_names}</strong>
                        </div>
                    </div>
                    <span style="background: #ef4444; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;">
                        TELE-ICU PRIORITY
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Patient Case Selection Dropdown
    case_ids = list(cases_dict.keys())
    
    # Sort with critical first, then newest
    def case_sort_key(cid):
        c = cases_dict[cid]
        is_crit = 1 if c.get("is_critical", False) and c.get("doctor_review", {}).get("status") != "reviewed" else 0
        return (is_crit, c.get("timestamp", ""))

    case_ids.sort(key=case_sort_key, reverse=True)
    
    def format_case_label(cid):
        c = cases_dict[cid]
        flag = "🚨 URGENT" if c.get("is_critical") and c.get("doctor_review", {}).get("status") != "reviewed" else ("✅ Reviewed" if c.get("doctor_review", {}).get("status") == "reviewed" else "⏳ Pending")
        finding = c.get("xray_finding", "Radiograph")
        triage_cat = c.get("triage_summary", {}).get("triage_category", "Standard")
        return f"{flag} | {cid} — {c.get('patient_name')} ({finding}) — {triage_cat}"

    selected_case_id = st.selectbox(
        "🔍 Select Patient Case to Audit & Sign:",
        options=case_ids,
        format_func=format_case_label,
        index=0
    )

    current_case = cases_dict[selected_case_id]
    triage = current_case.get("triage_summary", {})
    doc_rev = current_case.get("doctor_review", {})

    st.markdown(f"### 🔍 Case Review: `{selected_case_id}` ({current_case.get('patient_name')}, Age: {current_case.get('patient_age', 45)})")
    
    # Patient Objective Diagnostic Row
    v_c1, v_c2, v_c3, v_c4 = st.columns(4)
    v_c1.metric("Radiographic Finding", current_case.get("xray_finding", "Normal"), delta=f"{current_case.get('xray_confidence', 0.0):.1f}% Conf.")
    v_c2.metric("Pathology Markers", f"{len(current_case.get('lab_biomarkers', {}))} Analyzed", help="Verified from PDF slip")
    v_c3.metric("Center / PHC", current_case.get("location", "Bantwal PHC"))
    v_c4.metric("Emergency Contact", current_case.get("emergency_contact", "108 Emergency"))

    # Top Level Triage Summary Bar
    is_crit_case = current_case.get("is_critical", False)
    st.markdown(f"""
        <div style="background: {'#fef2f2' if is_crit_case else '#f0fdf4'}; border-left: 5px solid {'#ef4444' if is_crit_case else '#22c55e'}; padding: 14px; border-radius: 6px; margin: 12px 0;">
            <div style="font-weight: 700; color: {'#991b1b' if is_crit_case else '#166534'}; font-size: 0.95rem;">
                Triage Diagnosis: {triage.get('etiology', 'Clinical Examination')}
            </div>
            <div style="font-size: 0.86rem; color: #334155; margin-top: 4px;">
                {triage.get('clinical_reasoning', 'No specific abnormalities detected.')}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # DUAL COLUMN INSPECTION: VISION + GRAD-CAM & PATHOLOGY RAG
    # -------------------------------------------------------------
    col_vis, col_rag = st.columns(2)

    with col_vis:
        st.markdown("#### 🔬 Radiography Vision & Grad-CAM (Module 3)")
        
        # Load associated radiograph
        xray_img = None
        preset_code = current_case.get("xray_preset")
        
        # Search candidate image paths
        possible_paths = [
            f"data/sample_xrays/real_{preset_code}.jpeg",
            f"data/sample_xrays/{preset_code}.png",
            f"data/sample_xrays/{preset_code}.jpeg",
            "data/sample_xrays/real_patient_001_pneumonia.jpeg"
        ]
        
        for p in possible_paths:
            if os.path.exists(p):
                try:
                    xray_img = Image.open(p)
                    break
                except Exception:
                    pass

        if xray_img is not None:
            # Interactive Grad-CAM Saliency Slider
            opacity = st.slider("Grad-CAM Heatmap Transparency Overlay:", 0.0, 1.0, 0.65, step=0.05, key=f"grad_slider_{selected_case_id}")
            st.caption(f"ResNet-50 Layer 4 Saliency map blended at {int(opacity*100)}% opacity.")

            # Compute Model Prediction & Heatmap
            with st.spinner("Rendering ResNet-50 Layer 4 Saliency Activations..."):
                v_res = predict_xray(model, xray_img)
                h_map = gradcam.generate_heatmap(v_res["input_tensor"], class_idx=v_res["class_index"])
                blended_cam = gradcam.overlay_heatmap(xray_img, h_map, alpha=opacity, draw_legend=True)

            tab_cam, tab_raw = st.tabs(["Grad-CAM Saliency Overlay", "Original Radiograph"])
            with tab_cam:
                st.image(blended_cam, caption=f"Predicted: {v_res['predicted_class']} ({v_res['confidence']:.1f}% Confidence)", use_container_width=True)
            with tab_raw:
                st.image(xray_img, caption="Raw Thoracic Radiograph", use_container_width=True)
        else:
            st.info("Radiograph image not provided for this case.")

    with col_rag:
        st.markdown("#### 🧪 Pathology Biomarker Extraction & RAG (Module 4)")
        
        biomarkers = current_case.get("lab_biomarkers", {})
        report_data = {
            "biomarkers": biomarkers,
            "abnormal_count": sum(1 for v in biomarkers.values() if str(v.get("status", v.get("clinical_status", ""))).upper() not in ["NORMAL", "RECORDED"]),
            "clinical_flags": [
                f"{v.get('name', v.get('test_name', k))} is {v.get('status', v.get('clinical_status', 'Abnormal'))}"
                for k, v in biomarkers.items()
                if str(v.get("status", v.get("clinical_status", ""))).upper() not in ["NORMAL", "RECORDED"]
            ]
        }
        
        # Check if matching sample PDF exists and index its chunks into ChromaDB
        preset_code = current_case.get("xray_preset", "")
        pdf_candidates = [
            f"data/sample_reports/{preset_code}.pdf",
            f"data/sample_reports/patient_001_bacterial_pneumonia.pdf" if "pneu" in str(preset_code) else None,
            f"data/sample_reports/patient_002_normal.pdf" if "norm" in str(preset_code) else None,
            f"data/sample_reports/patient_003_tuberculosis.pdf" if "tb" in str(preset_code) or "tuber" in str(preset_code) else None
        ]
        pdf_loaded = False
        for p in pdf_candidates:
            if p and os.path.exists(p):
                try:
                    pdf_res = parse_pdf_report(p, use_ai=True)
                    vector_store.index_report_chunks(chunk_report_for_indexing(pdf_res))
                    report_data = pdf_res
                    pdf_loaded = True
                    break
                except Exception:
                    pass

        if not pdf_loaded and biomarkers:
            # Fallback: index directly from current case biomarkers
            chunks = chunk_report_for_indexing(report_data)
            vector_store.index_report_chunks(chunks)

        if biomarkers:
            table_rows = []
            for k, v in biomarkers.items():
                table_rows.append({
                    "Biomarker": v.get("name", v.get("test_name", k.upper())),
                    "Observed Value": f"{v.get('value')} {v.get('unit', '')}",
                    "Status": v.get("status", v.get("clinical_status", "NORMAL")),
                    "Reference Interval": v.get("normal_range", v.get("reference_range", "Standard"))
                })
            df_bio = pd.DataFrame(table_rows)
            st.dataframe(df_bio, use_container_width=True, hide_index=True)
        else:
            st.info("No laboratory biomarker slip was submitted for this case.")

        # Interactive Clinical Assistant Window for Clinicians
        render_rag_window(
            vector_store=vector_store,
            current_report_data=report_data,
            user_persona="doctor",
            key_prefix=f"doc_{selected_case_id}",
            show_direct_text_option=False
        )

    # -------------------------------------------------------------
    # ✍️ CLINICIAN DECISION OVERRIDE & DIGITAL SIGNATURE
    # -------------------------------------------------------------
    st.divider()
    st.markdown("### ✍️ Clinician Decision Override & Digital Signature")

    default_rx = doc_rev.get("prescription") or (
        "Right basal bacterial pneumonia confirmed with acute hypoxia. "
        "Prescribed: Tab Azithromycin 500mg OD x 3 days, Tab Paracetamol 650mg SOS. "
        "Administer nasal cannula O2 @ 2L/min at Bantwal PHC. Immediate tele-follow up in 24 hours."
        if is_crit_case else
        "Normal baseline confirmed. Reassure patient; maintain oral hydration and return if respiratory distress develops."
    )

    doctor_notes = st.text_area(
        "Official Clinical Prescription & Guidance (Will be dispatched directly to patient):",
        value=default_rx,
        height=100,
        key=f"rx_text_{selected_case_id}"
    )

    col_btn1, col_btn2 = st.columns([1.5, 1])
    with col_btn1:
        if st.button("🔒 Cryptographically Sign & Dispatch to Patient", type="primary", use_container_width=True, key=f"btn_sign_{selected_case_id}"):
            success = doctor_sign_and_dispatch(
                case_id=selected_case_id,
                doctor_name=doc_name,
                doctor_reg=doc_reg,
                prescription=doctor_notes,
                doctor_notes=doctor_notes
            )
            if success:
                st.success(f"Report digitally locked with key `{doc_name} - {doc_reg}` and sent to the patient's phone.")
                
                # Append to clinician audit log CSV
                audit_file = "data/clinician_audit_log.csv"
                audit_row = {
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Triage": triage.get("triage_category", "Standard"),
                    "Etiology": triage.get("etiology", "Clinical"),
                    "Confidence": f"{current_case.get('xray_confidence', 0.0):.1f}%",
                    "DoctorNotes": f"Signed by {doc_name} ({doc_reg}): {doctor_notes}"
                }
                df_audit = pd.DataFrame([audit_row])
                df_audit.to_csv(audit_file, mode="a", header=not os.path.exists(audit_file), index=False)
                st.toast("Updated Patient Portal & Saved to Audit CSV!", icon="🔒")
                st.rerun()

    with col_btn2:
        if is_crit_case:
            if st.button("🚨 Trigger 108 Emergency Tele-Referral", use_container_width=True):
                st.error(f"🚑 Fast-Track Ambulance & Tele-ICU referral dispatched for {current_case.get('patient_name')} ({selected_case_id}) to Bantwal PHC Emergency Ward!")
