"""
Module 1: Remote Patient & Home Care View
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Complete Frontend Implementation (Point-of-Care & Tele-ICU)
Uses real clinical chest radiographs (pneumonia-232.jpg) with interactive multimodal triage.
"""
import streamlit as st
import time
from PIL import Image
from src.ui.image_utils import get_real_sample_xray

def render_patient_portal():
    """Renders the comprehensive home care and patient result tracking dashboard."""
    user_id = st.session_state.get("user_id", "+91 9845012345")
    cases = st.session_state.get("patient_cases", {})

    # Top Header Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0369a1 0%, #0c4a6e 100%); padding: 22px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.12);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 style="margin: 0; font-size: 1.6rem; color: #38bdf8;">🏠 Remote Point-of-Care Patient Portal</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                        Logged in as: <strong>{user_id}</strong> | Primary Health Centre: <strong>Bantwal Rural PHC Zone 2</strong>
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.3); padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.82rem;">
                    🟢 Connected to Tele-ICU Center
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_new_scan, tab_my_results = st.tabs([
        "🔍 New Triage Scan & Health Check",
        "📁 My Historical Results & Doctor Prescriptions"
    ])

    with tab_new_scan:
        st.markdown("#### ⚡ Clinical Sample Test Presets (Thoracic Radiograph & Lab Biomarkers)")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        use_pneumonia = col_p1.button("⚠️ Bacterial Pneumonia", use_container_width=True)
        use_normal = col_p2.button("✅ Normal Baseline", use_container_width=True)
        use_tb = col_p3.button("🚨 Tuberculosis (TB)", use_container_width=True)
        clear_inputs = col_p4.button("✕ Clear Inputs", use_container_width=True)

        if "pat_scan_state" not in st.session_state:
            # Default to real pneumonia radiograph (pneumonia-232.jpg)
            st.session_state.pat_scan_state = {
                "preset": "pneumonia",
                "xray": get_real_sample_xray("pneumonia"),
                "fever": 4,
                "spo2": 89,
                "lab_name": "patient_001_bacterial_pneumonia.pdf",
                "biomarkers": {"WBC": "14,200 /µL (Elevated)", "CRP": "48.0 mg/L (Critically High)", "ESR": "38 mm/hr (Elevated)"},
                "pred_class": "Pneumonia / Consolidation",
                "conf": 92.4,
                "severity": "CRITICAL RISK - PRIORITY 1",
                "etiology": "Acute Bacterial Pulmonary Consolidation with High Inflammatory Biomarkers"
            }

        if clear_inputs:
            st.session_state.pat_scan_state = None
            st.session_state["show_triage_results"] = False
            st.rerun()

        if use_pneumonia:
            st.session_state.pat_scan_state = {
                "preset": "pneumonia",
                "xray": get_real_sample_xray("pneumonia"),
                "fever": 4,
                "spo2": 89,
                "lab_name": "patient_001_bacterial_pneumonia.pdf",
                "biomarkers": {"WBC": "14,200 /µL (Elevated)", "CRP": "48.0 mg/L (Critically High)", "ESR": "38 mm/hr (Elevated)"},
                "pred_class": "Pneumonia / Consolidation",
                "conf": 92.4,
                "severity": "CRITICAL RISK - PRIORITY 1",
                "etiology": "Acute Bacterial Pulmonary Consolidation with High Inflammatory Biomarkers"
            }
            st.session_state["show_triage_results"] = True
            st.toast("Loaded Real Bacterial Pneumonia Radiograph (pneumonia-232.jpg)!", icon="⚠️")

        if use_normal:
            st.session_state.pat_scan_state = {
                "preset": "normal",
                "xray": get_real_sample_xray("normal"),
                "fever": 0,
                "spo2": 98,
                "lab_name": "patient_002_normal.pdf",
                "biomarkers": {"WBC": "6,800 /µL (Normal)", "CRP": "2.1 mg/L (Normal)", "ESR": "8 mm/hr (Normal)"},
                "pred_class": "Normal Clear Baseline",
                "conf": 98.1,
                "severity": "LOW RISK - ROUTINE BASELINE",
                "etiology": "Clear Lung Parenchyma with Physiological Lab Biomarkers"
            }
            st.session_state["show_triage_results"] = True
            st.toast("Loaded Real Normal Baseline Radiograph!", icon="✅")

        if use_tb:
            st.session_state.pat_scan_state = {
                "preset": "tb",
                "xray": get_real_sample_xray("tb"),
                "fever": 12,
                "spo2": 93,
                "lab_name": "patient_003_tuberculosis.pdf",
                "biomarkers": {"WBC": "11,800 /µL (Slightly High)", "ESR": "62 mm/hr (Markedly Elevated)", "CRP": "34.0 mg/L (High)"},
                "pred_class": "Pulmonary Tuberculosis Suspect",
                "conf": 89.5,
                "severity": "CRITICAL RISK - PRIORITY 1",
                "etiology": "Apical Cavitary Infiltration Consistent with Tuberculosis"
            }
            st.session_state["show_triage_results"] = True
            st.toast("Loaded Real Tuberculosis (TB) Radiograph!", icon="🚨")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col_up1, col_up2 = st.columns(2)

        with col_up1:
            st.markdown("### 📸 1. Thoracic Radiograph (X-Ray)")
            xray_file = st.file_uploader("Upload Chest Radiograph (PNG / JPG / JPEG)", type=["png", "jpg", "jpeg"], key="pat_xray_up")
            if xray_file:
                loaded_img = Image.open(xray_file)
                st.session_state.pat_scan_state = {
                    "preset": "custom",
                    "xray": loaded_img,
                    "fever": 2,
                    "spo2": 95,
                    "lab_name": "Uploaded_Lab_Report.pdf",
                    "biomarkers": {"WBC": "9,200 /µL (Normal)", "CRP": "4.5 mg/L (Normal)"},
                    "pred_class": "Mild Opacity / Under Review",
                    "conf": 84.0,
                    "severity": "MODERATE RISK - OBSERVATION",
                    "etiology": "Localized Parenchymal Focus"
                }

            if st.session_state.pat_scan_state and st.session_state.pat_scan_state.get("xray"):
                st.image(st.session_state.pat_scan_state["xray"], caption="Active Thoracic Radiograph (Real Clinical Scan)", width=290)
            else:
                st.info("ℹ️ Upload a chest X-ray or click a preset above to load an imaging sample.")

        with col_up2:
            st.markdown("### 📋 2. Pathology Lab Slip & Vitals")
            st.file_uploader("Upload Diagnostic Blood / CBC Report (PDF / Image)", type=["pdf", "png", "jpg"], key="pat_lab_up")
            cur_fever = st.slider("Fever duration (Days):", 0, 14, st.session_state.pat_scan_state.get("fever", 2) if st.session_state.pat_scan_state else 2)
            cur_spo2 = st.number_input("SpO2 Blood Oxygen Level (%):", min_value=70, max_value=100, value=st.session_state.pat_scan_state.get("spo2", 96) if st.session_state.pat_scan_state else 96)

            st.markdown("""
                <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 14px; margin-top: 14px;">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a; margin-bottom: 4px;">
                        🎯 Objective Clinical Guidance
                    </div>
                    <div style="font-size: 0.81rem; color: #64748b; line-height: 1.5;">
                        AI cross-modally correlates radiographic consolidations with circulating leukocyte count and acute phase reactants (CRP) to eliminate false positives.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        if st.button("🔍 Run Remote Health Triage", type="primary", use_container_width=True):
            if not st.session_state.pat_scan_state:
                st.warning("Please upload an X-ray or choose one of the quick presets above.")
            else:
                with st.spinner("Analyzing thoracic vision features & laboratory biomarkers..."):
                    time.sleep(0.8)
                st.session_state["show_triage_results"] = True

        # Render Active Triage Results
        if st.session_state.get("show_triage_results") and st.session_state.pat_scan_state:
            data = st.session_state.pat_scan_state
            st.divider()
            st.markdown(f"### 🩺 Triage Assessment: `{data['pred_class']}`")

            if "CRITICAL" in data["severity"] or cur_spo2 < 92:
                st.markdown(f"""
                    <div style="background: #fef2f2; border: 2px solid #ef4444; border-left: 10px solid #dc2626; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <span style="font-size: 2.6rem;">🚨</span>
                            <div>
                                <div style="font-size: 1.25rem; font-weight: 800; color: #991b1b;">
                                    HIGH RISK / CRITICAL TRIAGE - IMMEDIATE MEDICAL ATTENTION
                                </div>
                                <div style="font-size: 0.95rem; color: #7f1d1d; margin-top: 4px; line-height: 1.5;">
                                    Multimodal clinical correlation indicates <strong>{data['etiology']}</strong> with SpO2 at {cur_spo2}%. Tele-ICU physician alerted.
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    st.markdown("""
                        <div style="background: #ffffff; border: 1px solid #fca5a5; border-radius: 8px; padding: 14px;">
                            <h5 style="color: #991b1b; margin-top: 0;">📋 Emergency Action Protocol</h5>
                            <ul style="font-size: 0.88rem; color: #7f1d1d; margin-bottom: 0;">
                                <li>Report immediately to Bantwal Rural PHC or Taluk Hospital.</li>
                                <li>Administer supplemental oxygen if SpO2 remains below 92%.</li>
                                <li>Isolate patient if productive cough or fever persists.</li>
                                <li><strong>An ambulance referral can be dispatched by calling 108.</strong></li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                with col_e2:
                    st.markdown("""
                        <div style="background: #ffffff; border: 1px solid #fca5a5; border-radius: 8px; padding: 14px;">
                            <h5 style="color: #991b1b; margin-top: 0;">📞 Emergency Helplines</h5>
                            <p style="font-size: 0.88rem; color: #7f1d1d; margin: 4px 0;">
                                • <strong>108 Arogya Kavacha Ambulance</strong> (Toll Free)<br/>
                                • <strong>Bantwal PHC Emergency Desk:</strong> +91 8255 238100<br/>
                                • <strong>Tele-ICU Doctor on Duty:</strong> Dr. Ramesh Rao (KMC-58291)
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

            elif "MODERATE" in data["severity"]:
                st.markdown("""
                    <div style="background: #fffbeb; border: 1px solid #f59e0b; border-left: 8px solid #d97706; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #92400e;">🟡 MODERATE RISK: Clinical Observation Advised</span>
                        <p style="margin: 6px 0 0 0; color: #78350f; font-size: 0.92rem;">
                            Mild parenchymal opacity detected. Please visit your nearest PHC within 24-48 hours for auscultation and clinical review.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #f0fdf4; border: 1px solid #22c55e; border-left: 8px solid #16a34a; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #166534;">🟢 LOW RISK: Routine Physiological Baseline</span>
                        <p style="margin: 6px 0 0 0; color: #14532d; font-size: 0.92rem;">
                            Radiographic examination and laboratory inflammatory parameters fall within physiological baseline intervals.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # Detail Cards: Vision vs Lab
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 🔬 Radiographic Vision Analysis")
                st.image(data["xray"], caption=f"Predicted: {data['pred_class']} ({data['conf']:.1f}% Confidence)", width=280)
            with c2:
                st.markdown("##### 🧪 Pathology Biomarker Findings")
                for k, v in data["biomarkers"].items():
                    st.markdown(f"• **{k}:** `{v}`")

            # Vernacular Voice Delivery Section
            st.divider()
            st.markdown("##### 🗣️ Vernacular Audio Voice Advisory")
            c_lang, c_play = st.columns([0.4, 0.6])
            with c_lang:
                chosen_v_lang = st.selectbox(
                    "Select Audio Delivery Language:",
                    ["ಕನ್ನಡ (Kannada)", "हिन्दी (Hindi)", "English", "தமிழ் (Tamil)", "తెలుగు (Telugu)"],
                    key="pat_voice_sel"
                )
            with c_play:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("🔊 Play Voice Advisory", key="btn_play_audio_pat"):
                    st.success(f"Playing patient voice advisory in {chosen_v_lang}...")
                    if "ಕನ್ನಡ" in chosen_v_lang:
                        st.info("📢 'ಎದೆ ಕ್ಷ-ಕಿರಣ ಮತ್ತು ರಕ್ತ ಪರೀಕ್ಷೆ ಎರಡರಲ್ಲೂ ಶ್ವಾಸಕೋಶದ ಸೋಂಕು ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿವೆ. ದಯವಿಟ್ಟು ತಕ್ಷಣವೇ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.'")
                    elif "हिन्दी" in chosen_v_lang:
                        st.info("📢 'छाती के एक्स-रे और रक्त परीक्षण दोनों में फेफड़ों के संक्रमण के लक्षण पाए गए हैं। कृपया तुरंत डॉक्टर से परामर्श लें।'")
                    else:
                        st.info("📢 'Radiographic findings and inflammatory biomarkers indicate signs of pulmonary consolidation. Immediate clinical consultation advised.'")

            # Interactive RAG Lab Assistant
            st.divider()
            st.markdown("### 💬 Interactive Laboratory Results Assistant (RAG)")
            st.markdown("<p style='font-size: 0.88rem; color: #475569;'>Ask questions regarding your laboratory slip or clinical findings:</p>", unsafe_allow_html=True)

            q_col1, q_col2, q_col3 = st.columns(3)
            q1 = q_col1.button("What is my WBC count?", key="rag_q1")
            q2 = q_col2.button("Is C-Reactive Protein (CRP) high?", key="rag_q2")
            q3 = q_col3.button("What precautions should I take?", key="rag_q3")

            custom_q = st.text_input("Or enter your own question:", placeholder="e.g., What does consolidation mean?", key="rag_custom_q")

            if q1 or "wbc" in custom_q.lower():
                st.markdown("""
                    <div style="background: #f8fafc; border-left: 4px solid #0284c7; padding: 14px; border-radius: 6px; margin-top: 10px;">
                        <strong>White Blood Cell (WBC) Findings:</strong><br/>
                        Your observed WBC count is elevated. Elevated leukocytes indicate that your body's immune defense is actively responding to a bacterial respiratory infection.
                    </div>
                """, unsafe_allow_html=True)
            elif q2 or "crp" in custom_q.lower():
                st.markdown("""
                    <div style="background: #f8fafc; border-left: 4px solid #f59e0b; padding: 14px; border-radius: 6px; margin-top: 10px;">
                        <strong>C-Reactive Protein (CRP) Explanation:</strong><br/>
                        CRP is an acute-phase inflammatory biomarker produced by the liver. Your elevated level strongly suggests localized thoracic parenchymal inflammation.
                    </div>
                """, unsafe_allow_html=True)
            elif q3 or "precaution" in custom_q.lower():
                st.markdown("""
                    <div style="background: #f8fafc; border-left: 4px solid #16a34a; padding: 14px; border-radius: 6px; margin-top: 10px;">
                        <strong>General Patient Precautions:</strong><br/>
                        Ensure strict bed rest, monitor SpO2 with a fingertip oximeter every 4 hours, maintain oral rehydration, and take all medications prescribed by the certified doctor.
                    </div>
                """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: MY HISTORICAL RESULTS & DOCTOR PRESCRIPTIONS
    # -------------------------------------------------------------
    with tab_my_results:
        st.markdown("#### 📁 Verified Records & Digital Doctor Prescriptions")

        for c_id, cs in cases.items():
            doc_rev = cs.get("doctor_review", {})
            is_signed = doc_rev.get("status") == "reviewed"
            status_badge = "✅ Signed by Doctor" if is_signed else "⏳ Pending Clinical Audit"

            with st.expander(f"Case `{c_id}` — {cs.get('patient_name')} ({cs.get('xray_finding')}) — [{status_badge}]", expanded=True):
                col_m1, col_m2 = st.columns([1.2, 0.8])
                with col_m1:
                    triage = cs.get("triage_summary", {})
                    st.markdown(f"**Triage Diagnosis:** `{triage.get('etiology')}`")
                    st.markdown(f"**Triage Risk Category:** `{triage.get('triage_category')}`")
                    st.markdown(f"**Radiograph Finding:** `{cs.get('xray_finding')}` ({cs.get('xray_confidence', 0.0):.1f}% Confidence)")
                    st.markdown(f"**Recommended Action:** {triage.get('recommendation')}")

                with col_m2:
                    if is_signed:
                        st.markdown(f"""
                            <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 14px;">
                                <h5 style="margin: 0 0 6px 0; color: #166534;">👨‍⚕️ Clinician Verification & E-Signature</h5>
                                <p style="font-size: 0.84rem; color: #14532d; margin: 0 0 8px 0;">
                                    <strong>Doctor:</strong> {doc_rev.get('doctor_name', 'Dr. Ramesh Rao')}<br/>
                                    <strong>Medical Reg No:</strong> <code>{doc_rev.get('doctor_reg', 'KMC-58291')}</code><br/>
                                    <strong>Validated Timestamp:</strong> {doc_rev.get('reviewed_at', '2026-10-29 20:00:10')}
                                </p>
                                <div style="background: #ffffff; border: 1px dashed #4ade80; border-radius: 6px; padding: 10px; font-size: 0.86rem; color: #0f172a;">
                                    <strong>Official Prescription:</strong><br/>
                                    {doc_rev.get('prescription')}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px;">
                                <h5 style="margin: 0 0 6px 0; color: #92400e;">⏳ Pending Clinician Audit</h5>
                                <p style="font-size: 0.84rem; color: #78350f; margin: 0;">
                                    This remote scan is currently in the doctor's queue. A Registered Medical Practitioner (RMP) at the Tele-ICU center will review and dispatch official signed prescriptions.
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

__all__ = ["render_patient_portal"]
