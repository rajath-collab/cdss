"""
Module 1: Remote Patient & Home Care View
Lead: Student 1 (System Architect)
Integrates:
  - Student 2 (Module 3): Vision ResNet-50 & Grad-CAM
  - Student 3 (Module 4): Pathology RAG & ChromaDB
  - Full Vernacular Localization Engine (English, Kannada, Hindi, Tamil, Telugu)
  - Remote Doctor Emergency Alert & Prescription Dispatch
"""

import os
import time
from PIL import Image
import streamlit as st
import pandas as pd

from models.vision_model import predict_xray
from rag.parser import extract_text_from_pdf, parse_clinical_biomarkers, chunk_report_for_indexing, parse_pdf_report
from models.fusion import fuse_clinical_modalities
from voice.tts_engine import synthesize_clinical_audio, get_clinical_speech_text, VERNACULAR_TEMPLATES
from utils.case_manager import save_patient_submission, get_patient_cases
from modules.rag_component import render_rag_window
from utils.translations import get_ui_text, LANGUAGES


def render_patient_portal(current_user: dict = None, model = None, gradcam = None, vector_store = None):
    """Renders the comprehensive home care and patient result tracking dashboard with full multi-lingual localization."""
    if current_user is None:
        current_user = st.session_state.get("current_user") or {
            "role": "patient",
            "full_name": "Rajesh Kumar",
            "username": "patient.rajesh",
            "patient_id": "PT-2026-8491",
            "location": "Bantwal Rural PHC"
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
    # 🛡️ STRICT SERVER-SIDE ROLE GUARD
    # -------------------------------------------------------------
    if current_user.get("role") not in ["patient", "asha"]:
        st.error("⛔ Access Denied: This portal is configured for Patient Home Care & ASHA field tracking.")
        st.info("Clinicians should utilize the Clinician Diagnostic Console.")
        st.stop()
        
    patient_name = current_user.get("full_name", "Patient")
    patient_username = current_user.get("username", "patient")
    patient_id = current_user.get("patient_id", f"PT-2026-{patient_username}")

    # Initialize and fetch active UI language
    if "ui_lang" not in st.session_state:
        st.session_state["ui_lang"] = "en"
    ui_lang = st.session_state.get("ui_lang", "en")
    t = get_ui_text(ui_lang)

    # -------------------------------------------------------------
    # 🌐 DYNAMIC LANGUAGE SELECTOR BAR
    # -------------------------------------------------------------
    col_lang_info, col_lang_dropdown = st.columns([0.65, 0.35])
    with col_lang_info:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; padding-top: 8px;">
                <span style="font-size: 1.25rem;">🌐</span>
                <span style="font-size: 0.96rem; font-weight: 700; color: #0284c7;">
                    {t['lang_selector_label']}
                </span>
            </div>
        """, unsafe_allow_html=True)
    with col_lang_dropdown:
        lang_keys = list(LANGUAGES.keys())
        cur_lang_idx = lang_keys.index(ui_lang) if ui_lang in lang_keys else 0
        selected_lang = st.selectbox(
            "Select Portal Language",
            lang_keys,
            index=cur_lang_idx,
            format_func=lambda k: f"{LANGUAGES[k]['flag']} {LANGUAGES[k]['native']}",
            key="patient_portal_lang_select_box",
            label_visibility="collapsed"
        )
        if selected_lang != ui_lang:
            st.session_state["ui_lang"] = selected_lang
            st.rerun()

    # -------------------------------------------------------------
    # 🏠 PATIENT PORTAL HEADER BANNER
    # -------------------------------------------------------------
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0369a1 0%, #0c4a6e 100%); padding: 22px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.12);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 style="margin: 0; font-size: 1.6rem; color: #38bdf8;">{t['patient_portal_title']}</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                        {t['logged_in_as']} <strong>{patient_name}</strong> | {t['patient_id_label']} <code>{patient_id}</code> | {t['phc_label']} {current_user.get('location', 'Bantwal Rural')}
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.82rem;">
                    {t['connected_tele_icu']}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Top Tabs: New Triage Scan vs My Historical Results & Doctor Prescriptions
    tab_new_scan, tab_my_results = st.tabs([t["tab_new_scan"], t["tab_my_results"]])

    with tab_new_scan:
        st.markdown(f"#### {t['upload_section_title']}")
        
        # Preset Quick Loaders for seamless testing
        st.markdown(f"<p style='font-size: 0.82rem; font-weight: 600; color: #475569; margin-bottom: 6px;'>{t['presets_label']}</p>", unsafe_allow_html=True)
        col_ps1, col_ps2, col_ps3, col_ps4 = st.columns(4)
        use_pneumonia_preset = col_ps1.button(t["preset_pneumonia"], key="btn_p_pneu")
        use_normal_preset = col_ps2.button(t["preset_normal"], key="btn_p_norm")
        use_tb_preset = col_ps3.button(t["preset_tb"], key="btn_p_tb")
        reset_patient_inputs = col_ps4.button(t["preset_clear"], key="btn_p_clear")

        if "pat_xray_img" not in st.session_state:
            st.session_state.pat_xray_img = None
        if "pat_pdf_bytes" not in st.session_state:
            st.session_state.pat_pdf_bytes = None
        if "pat_preset_name" not in st.session_state:
            st.session_state.pat_preset_name = None
        if "pat_latest_triage" not in st.session_state:
            st.session_state.pat_latest_triage = None

        if reset_patient_inputs:
            st.session_state.pat_xray_img = None
            st.session_state.pat_pdf_bytes = None
            st.session_state.pat_preset_name = None
            st.session_state.pat_latest_triage = None
            st.rerun()

        if use_pneumonia_preset:
            img_p = "data/sample_xrays/real_patient_001_pneumonia.jpeg"
            pdf_p = "data/sample_reports/patient_001_bacterial_pneumonia.pdf"
            if os.path.exists(img_p):
                st.session_state.pat_xray_img = Image.open(img_p)
            if os.path.exists(pdf_p):
                with open(pdf_p, "rb") as f:
                    st.session_state.pat_pdf_bytes = f.read()
            st.session_state.pat_preset_name = "patient_001_pneumonia"
            st.toast(t["toast_pneumonia"], icon="⚠️")

        if use_normal_preset:
            img_p = "data/sample_xrays/real_patient_002_normal.jpeg"
            pdf_p = "data/sample_reports/patient_002_normal.pdf"
            if os.path.exists(img_p):
                st.session_state.pat_xray_img = Image.open(img_p)
            if os.path.exists(pdf_p):
                with open(pdf_p, "rb") as f:
                    st.session_state.pat_pdf_bytes = f.read()
            st.session_state.pat_preset_name = "patient_002_normal"
            st.toast(t["toast_normal"], icon="✅")

        if use_tb_preset:
            img_p = "data/sample_xrays/real_patient_003_tuberculosis.jpeg"
            pdf_p = "data/sample_reports/patient_003_tuberculosis.pdf"
            if os.path.exists(img_p):
                st.session_state.pat_xray_img = Image.open(img_p)
            if os.path.exists(pdf_p):
                with open(pdf_p, "rb") as f:
                    st.session_state.pat_pdf_bytes = f.read()
            st.session_state.pat_preset_name = "patient_003_tuberculosis"
            st.toast(t["toast_tb"], icon="🚨")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"### {t['col_xray_title']}")
            uploaded_xray = st.file_uploader(t["upload_xray_prompt"], type=["png", "jpg", "jpeg"], key="p_xray_file")
            if uploaded_xray is not None:
                st.session_state.pat_xray_img = Image.open(uploaded_xray)
                st.session_state.pat_preset_name = "custom_upload"

            if st.session_state.pat_xray_img:
                st.image(st.session_state.pat_xray_img, caption=t["active_xray_caption"], width=300)

        with col2:
            st.markdown(f"### {t['col_lab_title']}")
            uploaded_lab = st.file_uploader(t["upload_lab_prompt"], type=["pdf"], key="p_lab_file")
            if uploaded_lab is not None:
                st.session_state.pat_pdf_bytes = uploaded_lab.read()
                st.session_state.pat_preset_name = "custom_upload"

            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 14px; margin-top: 14px;">
                <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a; margin-bottom: 4px;">
                    {t['objective_title']}
                </div>
                <div style="font-size: 0.81rem; color: #64748b; line-height: 1.5;">
                    {t['objective_desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Submission Button
        if st.button(t["btn_run_triage"], type="primary", use_container_width=True):
            if not st.session_state.pat_xray_img and not st.session_state.pat_pdf_bytes:
                st.warning(t["warning_no_input"])
            else:
                with st.spinner(t["spinner_analyzing"]):
                    time.sleep(0.5)
                    
                    # 1. Vision Inference (Module 3)
                    vision_res = None
                    heatmap = None
                    if st.session_state.pat_xray_img:
                        vision_res = predict_xray(model, st.session_state.pat_xray_img)
                        heatmap = gradcam.generate_heatmap(
                            vision_res["input_tensor"],
                            class_idx=vision_res["class_index"]
                        )
                    
                    # 2. Pathology RAG Parsing (Module 4)
                    parsed_lab = None
                    if st.session_state.pat_pdf_bytes:
                        report_text = extract_text_from_pdf(st.session_state.pat_pdf_bytes)
                        parsed_lab = parse_clinical_biomarkers(report_text)
                        chunks = chunk_report_for_indexing(parsed_lab)
                        vector_store.index_report_chunks(chunks)

                    # 3. Multimodal Clinical Correlation
                    fusion_summary = fuse_clinical_modalities(vision_res, parsed_lab)

                    # 4. Save to Case Manager for Remote Doctor Review
                    new_case_id = save_patient_submission(
                        patient_username=patient_username,
                        patient_name=patient_name,
                        vision_results=vision_res,
                        lab_results=parsed_lab,
                        fusion_summary=fusion_summary,
                        xray_preset=st.session_state.pat_preset_name
                    )

                    st.session_state.pat_latest_triage = {
                        "case_id": new_case_id,
                        "vision_res": vision_res,
                        "parsed_lab": parsed_lab,
                        "fusion_summary": fusion_summary
                    }

        # Render Active Triage Results if available
        if st.session_state.get("pat_latest_triage") is not None:
            triage_data = st.session_state.pat_latest_triage
            new_case_id = triage_data["case_id"]
            vision_res = triage_data["vision_res"]
            parsed_lab = triage_data["parsed_lab"]
            fusion_summary = triage_data["fusion_summary"]

            st.divider()
            st.markdown(f"### {t['assessment_title']} (`{t['case_label']}: {new_case_id}`)")

            # -------------------------------------------------------------
            # 🚨 EMERGENCY RISK CHECK
            # -------------------------------------------------------------
            is_ai_critical = "HIGH" in fusion_summary["triage_category"] or "CRITICAL" in fusion_summary["triage_category"]

            if is_ai_critical:
                etiology_text = fusion_summary.get('etiology', 'Acute Pulmonary Infiltration')
                alert_desc = t["critical_alert_desc"].replace("{etiology}", f"<strong>{etiology_text}</strong>")
                st.markdown(f"""
                    <div style="background: #fef2f2; border: 2px solid #ef4444; border-left: 10px solid #dc2626; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <span style="font-size: 2.6rem;">🚨</span>
                            <div>
                                <div style="font-size: 1.25rem; font-weight: 800; color: #991b1b;">
                                    {t['critical_alert_badge']}
                                </div>
                                <div style="font-size: 0.95rem; color: #7f1d1d; margin-top: 4px; line-height: 1.5;">
                                    {alert_desc}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                col_em1, col_em2 = st.columns(2)
                with col_em1:
                    st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #fca5a5; border-radius: 8px; padding: 14px;">
                            <h5 style="color: #991b1b; margin-top: 0;">{t['emergency_protocol_title']}</h5>
                            <ul style="font-size: 0.88rem; color: #7f1d1d; margin-bottom: 0;">
                                <li>{t['emergency_proto_1']}</li>
                                <li>{t['emergency_proto_2']}</li>
                                <li>{t['emergency_proto_3']}</li>
                                <li><strong>{t['emergency_proto_4']}</strong></li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                with col_em2:
                    st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #fca5a5; border-radius: 8px; padding: 14px;">
                            <h5 style="color: #991b1b; margin-top: 0;">{t['contacts_title']}</h5>
                            <p style="font-size: 0.88rem; color: #7f1d1d; margin: 4px 0;">
                                • <strong>{t['contact_hotline']}</strong><br/>
                                • <strong>{t['contact_phc']}</strong><br/>
                                • <strong>{t['contact_doc']}</strong>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

            elif "MODERATE" in fusion_summary["triage_category"]:
                st.markdown(f"""
                    <div style="background: #fffbeb; border: 1px solid #f59e0b; border-left: 8px solid #d97706; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #92400e;">{t['moderate_risk_title']}</span>
                        <p style="margin: 6px 0 0 0; color: #78350f; font-size: 0.92rem;">
                            {t['moderate_risk_desc']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: #f0fdf4; border: 1px solid #22c55e; border-left: 8px solid #16a34a; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #166534;">{t['low_risk_title']}</span>
                        <p style="margin: 6px 0 0 0; color: #14532d; font-size: 0.92rem;">
                            {t['low_risk_desc']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # Show Model & RAG Findings
            c_res1, c_res2 = st.columns(2)
            with c_res1:
                st.markdown(f"##### {t['vision_card_title']}")
                if vision_res:
                    pred_txt = f"{t['pred_label']} {vision_res['predicted_class']} ({vision_res['confidence']:.1f}%)"
                    st.image(vision_res["enhanced_image"], caption=pred_txt, width=280)
                else:
                    st.info(t["vision_no_img"])

            with c_res2:
                st.markdown(f"##### {t['biomarker_card_title']}")
                if parsed_lab and parsed_lab.get("biomarkers"):
                    b_list = []
                    for k, v in parsed_lab["biomarkers"].items():
                        raw_name = v.get("name") or v.get("test_name", k.upper())
                        localized_name = t["biomarkers"].get(k.lower(), raw_name)
                        val = v.get("value", "")
                        unit = v.get("unit", "")
                        raw_stat = v.get("status") or v.get("clinical_status", "NORMAL")
                        localized_stat = t["statuses"].get(raw_stat.upper(), raw_stat)
                        b_list.append(f"• **{localized_name}:** {val} {unit} (`{localized_stat}`)")
                    st.markdown("\n".join(b_list))
                else:
                    st.info(t["biomarker_no_slip"])

            # Vernacular Audio Playback for Patient (Auto-syncs with chosen UI language)
            st.divider()
            st.markdown(f"##### {t['voice_section_title']}")
            
            # Default audio language to active ui_lang if supported in tts, otherwise kn
            tts_langs = list(VERNACULAR_TEMPLATES.keys())
            audio_default_idx = tts_langs.index(ui_lang) if ui_lang in tts_langs else 0
            
            v_lang = st.selectbox(
                t["choose_audio_lang"],
                tts_langs,
                index=audio_default_idx,
                format_func=lambda x: VERNACULAR_TEMPLATES[x]["name"],
                key="p_audio_lang"
            )
            spoken_vern, spoken_eng, _ = get_clinical_speech_text(fusion_summary, language=v_lang)
            st.caption(f'"{spoken_vern}"')
            
            if st.button(t["btn_play_audio"], key="btn_play_patient_audio"):
                with st.spinner(t["spinner_voice"]):
                    audio_data = synthesize_clinical_audio(
                        diagnosis_type=fusion_summary["etiology"],
                        language=v_lang,
                        fusion_summary=fusion_summary
                    )
                    if audio_data:
                        st.audio(audio_data, format="audio/mp3")

        # -------------------------------------------------------------
        # 💬 INTERACTIVE PATIENT LAB ASSISTANT
        # -------------------------------------------------------------
        st.divider()
        st.markdown(f"### {t['lab_assist_title']}")
        st.markdown(f"<p style='font-size: 0.88rem; color: #475569;'>{t['lab_assist_desc']}</p>", unsafe_allow_html=True)
        
        active_patient_report = None
        if st.session_state.get("pat_latest_triage") is not None:
            active_patient_report = st.session_state.pat_latest_triage.get("parsed_lab")

        render_rag_window(
            vector_store=vector_store,
            current_report_data=active_patient_report,
            current_pdf_bytes=st.session_state.pat_pdf_bytes,
            user_persona="patient",
            key_prefix="patient_triage_rag",
            show_direct_text_option=False
        )

    # -----------------------------------------------------------------
    # TAB 2: MY PAST RESULTS & DOCTOR PRESCRIPTIONS
    # -----------------------------------------------------------------
    with tab_my_results:
        st.markdown(f"#### {t['past_results_title']}")
        
        my_cases = get_patient_cases(patient_username)
        if not my_cases:
            st.info(t["no_cases_yet"])
        else:
            for idx, cs in enumerate(my_cases):
                c_id = cs.get("case_id")
                c_time = cs.get("timestamp")
                doc_rev = cs.get("doctor_review", {})
                is_reviewed = doc_rev.get("status") == "reviewed"
                triage = cs.get("triage_summary", {})
                status_badge = t["status_signed"] if is_reviewed else t["status_pending"]

                with st.expander(f"📁 {t['case_label']} `{c_id}` — {c_time} — [{status_badge}]", expanded=(idx==0)):
                    col_m1, col_m2 = st.columns([1.2, 0.8])
                    with col_m1:
                        st.markdown(f"**{t['label_triage_diag']}** `{triage.get('etiology', 'Clinical Examination')}`")
                        st.markdown(f"**{t['label_triage_level']}** `{triage.get('triage_category', 'Standard')}`")
                        st.markdown(f"**{t['label_scan_finding']}** `{cs.get('xray_finding', 'Radiograph Verified')}` ({cs.get('xray_confidence', 0.0):.1f}%) | **{t['label_biomarkers_eval']}** `{len(cs.get('lab_biomarkers', {}))}`")
                        st.markdown(f"**{t['label_recommendation']}** {triage.get('recommendation', 'Routine follow-up')}")

                    with col_m2:
                        if is_reviewed:
                            st.markdown(f"""
                                <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 14px;">
                                    <h5 style="margin: 0 0 6px 0; color: #166534;">{t['clinician_review_card']}</h5>
                                    <p style="font-size: 0.84rem; color: #14532d; margin: 0 0 8px 0;">
                                        <strong>{t['rev_doctor']}</strong> {doc_rev.get("doctor_name", "Registered Medical Practitioner")}<br/>
                                        <strong>{t['rev_reg']}</strong> {doc_rev.get("doctor_reg", "KMC-RMP")}<br/>
                                        <strong>{t['rev_signed']}</strong> {doc_rev.get("reviewed_at", "Verified")}
                                    </p>
                                    <div style="background: #ffffff; border: 1px dashed #4ade80; border-radius: 6px; padding: 10px; font-size: 0.86rem; color: #0f172a;">
                                        <strong>{t['rev_prescription']}</strong><br/>
                                        {doc_rev.get("prescription", "Take plenty of fluids and rest.")}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px;">
                                    <h5 style="margin: 0 0 6px 0; color: #92400e;">{t['pending_audit_title']}</h5>
                                    <p style="font-size: 0.84rem; color: #78350f; margin: 0;">
                                        {t['pending_audit_desc']}
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
