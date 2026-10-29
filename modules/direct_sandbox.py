"""
Module 5: Direct Multimodal Ingestion Sandbox & ASHA Frontline Advisory
Part of Multimodal Fused Clinical Decision Support System (CDSS)
"""

import os
import json
import pandas as pd
from PIL import Image
import streamlit as st

from models.vision_model import predict_xray
from models.gradcam import GradCAM
from models.fusion import fuse_clinical_modalities
from rag.parser import extract_text_from_pdf, parse_clinical_biomarkers, chunk_report_for_indexing
from voice.tts_engine import synthesize_clinical_audio, get_clinical_speech_text, VERNACULAR_TEMPLATES
from modules.rag_component import render_rag_window


def render_direct_sandbox(app_mode: str = "Multimodal Ingestion", model = None, gradcam = None, vector_store = None):
    """Renders the standalone multimodal ingestion, presets, and frontline ASHA voice triage."""
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
    
    # Session State Management for Sample Presets
    if "xray_file" not in st.session_state:
        st.session_state.xray_file = None
    if "pdf_file" not in st.session_state:
        st.session_state.pdf_file = None

    # Modality Ingestion Section
    col_up1, col_up2 = st.columns(2)

    with col_up1:
        st.subheader("1. Thoracic Radiograph (X-Ray)")
        uploaded_xray = st.file_uploader(
            "Upload Frontal Chest Radiograph (PNG / JPEG)",
            type=["png", "jpg", "jpeg"],
            key="sandbox_xray_uploader"
        )
        if uploaded_xray is not None:
            st.session_state.xray_file = Image.open(uploaded_xray)

    with col_up2:
        st.subheader("2. Pathology Lab Slip (PDF)")
        uploaded_pdf = st.file_uploader(
            "Upload Diagnostic Lab Slip (PDF)",
            type=["pdf"],
            key="sandbox_pdf_uploader"
        )
        if uploaded_pdf is not None:
            st.session_state.pdf_file = uploaded_pdf.read()

    # Execution Trigger
    has_xray = st.session_state.xray_file is not None
    has_pdf = st.session_state.pdf_file is not None

    if has_xray or has_pdf:
        current_xray = st.session_state.xray_file
        current_pdf_bytes = st.session_state.pdf_file
        
        with st.spinner("Processing Clinical Ingestion & AI Diagnostic Pipelines..."):
            # Vision Pipeline
            vision_res = None
            heatmap = None
            if has_xray:
                vision_res = predict_xray(model, current_xray)
                heatmap = gradcam.generate_heatmap(
                    vision_res["input_tensor"],
                    class_idx=vision_res["class_index"]
                )
                
            # Report Parsing Pipeline
            parsed_lab = None
            if has_pdf:
                report_text = extract_text_from_pdf(current_pdf_bytes)
                parsed_lab = parse_clinical_biomarkers(report_text)
                chunks = chunk_report_for_indexing(parsed_lab)
                vector_store.index_report_chunks(chunks)
                
            # Multimodal / Standalone Clinical Correlation
            fusion_summary = fuse_clinical_modalities(vision_res, parsed_lab)

        # Dynamic Mode Indicators
        if has_xray and has_pdf:
            mode_badge = "🔀 MULTIMODAL FUSED CLINICAL TRIAGE"
            mode_color = "#1e3e62"
        elif has_xray and not has_pdf:
            mode_badge = "🫁 STANDALONE THORACIC RADIOGRAPH (X-RAY) ANALYSIS"
            mode_color = "#92400e"
        else:
            mode_badge = "🧪 STANDALONE PATHOLOGY LAB BIOMARKER ANALYSIS"
            mode_color = "#0369a1"

        # -------------------------------------------------------------
        # PERSONA VIEW: ASHA / FRONTLINE WORKER (FIELD MODE)
        # -------------------------------------------------------------
        if "ASHA" in app_mode:
            st.divider()
            st.subheader("🤝 ASHA & Frontline Point-of-Care Advisory")
            
            # Triage Category & Risk Level
            triage_cat = fusion_summary.get("triage_category", "")
            is_high_risk = "HIGH" in triage_cat or "CRITICAL" in triage_cat
            is_moderate_risk = "MODERATE" in triage_cat or "OBSERVATION" in triage_cat
            
            if is_high_risk:
                st.error("🚨 **ತುರ್ತು ಕ್ರಮ ಅಗತ್ಯವಿದೆ (HIGH RISK / URGENT ATTENTION)**\n\n"
                         "Patient shows concordant evidence of acute pulmonary infection or active cavitary lesions. "
                         "Refer immediately to Medical Officer / Primary Health Centre (PHC).")
            elif is_moderate_risk:
                st.warning("⚠️ **ವೈದ್ಯರ ನೇರ ತಪಾಸಣೆ ಅಗತ್ಯವಿದೆ (CLINICAL OBSERVATION REQUIRED)**\n\n"
                           f"**ವಿವರಣೆ (Findings):** {fusion_summary['clinical_reasoning']}\n\n"
                           f"**ಮುಂದಿನ ಕ್ರಮ (Field Action):** {fusion_summary['recommendation']}")
            else:
                st.success("✅ **ಸಾಮಾನ್ಯ ಫಲಿತಾಂಶ (ROUTINE CARE / NORMAL BASELINE)**\n\n"
                           "Clear lung fields and normal inflammatory biomarkers. No acute consolidation detected. Provide routine care.")

            c_asha1, c_asha2 = st.columns([1, 1])
            
            spoken_vernacular, spoken_english, condition_key = get_clinical_speech_text(
                fusion_summary=fusion_summary,
                language="kn"
            )
            
            with c_asha1:
                st.markdown("### 🎙️ Vernacular Speech Synthesis (ಗ್ರಾಮೀಣ ಧ್ವನಿ ಸೌಲಭ್ಯ)")
                selected_lang = st.selectbox(
                    "Select Consultation Language:",
                    options=list(VERNACULAR_TEMPLATES.keys()),
                    format_func=lambda x: VERNACULAR_TEMPLATES[x]["name"],
                    index=0,
                    key="asha_speech_lang_select"
                )
                
                spoken_vernacular, spoken_english, condition_key = get_clinical_speech_text(
                    fusion_summary=fusion_summary,
                    language=selected_lang
                )
                
                if st.button("🔊 Play Vernacular Audio Instructions", type="primary", use_container_width=True, key="btn_asha_play_audio"):
                    with st.spinner("Synthesizing vernacular speech..."):
                        audio_data = synthesize_clinical_audio(
                            diagnosis_type=fusion_summary["etiology"],
                            language=selected_lang,
                            fusion_summary=fusion_summary
                        )
                        if audio_data:
                            st.audio(audio_data, format="audio/mp3")
                        else:
                            st.warning("⚠️ Speech synthesis engine is currently running in text-only mode.")
                
                st.markdown(f"""
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px 16px; margin-top: 12px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: #0f172a; margin-bottom: 6px;">
                        🗣️ Spoken Clinical Advice ({VERNACULAR_TEMPLATES[selected_lang]['name']}):
                    </div>
                    <div style="font-size: 0.92rem; color: #1e293b; line-height: 1.5; margin-bottom: 10px; font-weight: 500;">
                        "{spoken_vernacular}"
                    </div>
                    <div style="font-size: 0.78rem; color: #64748b; border-top: 1px dashed #cbd5e1; padding-top: 8px; line-height: 1.4;">
                        <strong>🌐 English Translation:</strong> "{spoken_english}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c_asha2:
                st.markdown("### 📝 Simplified Clinical Summary")
                chest_summary = f"{vision_res['predicted_class']} ({vision_res['confidence']:.1f}%)" if vision_res else "Not Uploaded (Pending Scan)"
                abnormal_cnt = parsed_lab.get('abnormal_count', 0) if parsed_lab else 0
                lab_summary = f"{abnormal_cnt} markers outside normal range" if parsed_lab else "Not Uploaded (Pending Lab Slip)"
                
                st.markdown(f"""
                - **Triage Level:** `{fusion_summary['triage_category']}`
                - **Chest Condition:** {chest_summary}
                - **Infection Markers:** {lab_summary}
                - **Field Action:** {fusion_summary['recommendation']}
                """)

        # -------------------------------------------------------------
        # PERSONA VIEW: DIRECT INGESTION & DIAGNOSTIC SANDBOX
        # -------------------------------------------------------------
        else:
            st.divider()
            c_head1, c_head2 = st.columns([0.65, 0.35])
            with c_head1:
                st.subheader("🔬 Multimodal Triage Sandbox")
            with c_head2:
                st.markdown(
                    f"<div style='text-align: right; padding-top: 10px;'>"
                    f"<span style='background: {mode_color}; color: #ffffff; padding: 5px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;'>"
                    f"{mode_badge}</span></div>",
                    unsafe_allow_html=True
                )
            
            is_urgent = "HIGH" in fusion_summary["triage_category"] or "CRITICAL" in fusion_summary["triage_category"]
            badge_class = "badge-urgent" if is_urgent else "badge-normal"
            st.markdown(f"""
            <div style="background: {'#fef2f2' if is_urgent else '#f0fdf4'}; border-left: 5px solid {'#ef4444' if is_urgent else '#22c55e'}; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="{badge_class}">{fusion_summary['triage_category']}</span>
                        <h3 style="margin: 8px 0 4px 0; color: #0f172a;">{fusion_summary['etiology']}</h3>
                        <p style="margin: 0; color: #475569; font-size: 0.95rem;">{fusion_summary['clinical_reasoning']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_vis, c_lab = st.columns([1, 1])
            with c_vis:
                st.markdown("### 🔬 Radiography & Grad-CAM Localization")
                if has_xray:
                    cam_alpha = st.slider(
                        "Grad-CAM Heatmap Opacity",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.55,
                        step=0.05,
                        key="sandbox_cam_alpha"
                    )
                    overlay_img = gradcam.overlay_heatmap(current_xray, heatmap, alpha=cam_alpha, draw_legend=True)
                    st.image(overlay_img, caption=f"Grad-CAM on layer4 (Confidence: {vision_res['confidence']:.1f}%)", use_container_width=True)
                else:
                    st.info("Thoracic Radiograph Not Uploaded.")

            with c_lab:
                st.markdown("### 🧪 Pathology Slip Biomarkers (RAG)")
                if has_pdf and parsed_lab and parsed_lab.get("biomarkers"):
                    table_rows = []
                    for k, v in parsed_lab["biomarkers"].items():
                        table_rows.append({
                            "Biomarker": v.get("name", v.get("test_name", k.upper())),
                            "Value": f"{v.get('value', '')} {v.get('unit', '')}",
                            "Status": v.get("status", v.get("clinical_status", "NORMAL")),
                            "Reference Interval": v.get("normal_range", v.get("reference_range", "Standard"))
                        })
                    df = pd.DataFrame(table_rows)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Pathology Lab Slip Not Uploaded.")

                # Interactive RAG Window in Sandbox
                render_rag_window(
                    vector_store=vector_store,
                    current_report_data=parsed_lab,
                    current_pdf_bytes=current_pdf_bytes,
                    user_persona="clinician",
                    key_prefix="sandbox_rag",
                    show_direct_text_option=True
                )

            # Model Performance Expander
            st.divider()
            with st.expander("📊 Model Training & Clinical Evaluation Metrics (ResNet-50 Benchmark)", expanded=False):
                if os.path.exists("data/model_metrics.json"):
                    with open("data/model_metrics.json", "r") as mf:
                        met = json.load(mf)
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Test Accuracy", f"{met['test_accuracy']}%")
                    m2.metric("Sensitivity (Recall)", f"{met['sensitivity']}%")
                    m3.metric("Specificity", f"{met['specificity']}%")
                    m4.metric("Precision", f"{met['precision']}%")
                    
                    c_p1, c_p2 = st.columns(2)
                    if os.path.exists("data/training_curves.png"):
                        c_p1.image("data/training_curves.png", caption="Loss / Accuracy Curves", use_container_width=True)
                    if os.path.exists("data/confusion_matrix.png"):
                        c_p2.image("data/confusion_matrix.png", caption="Clinical Confusion Matrix", use_container_width=True)

    else:
        st.info("👈 **Get Started:** Upload a Chest X-ray, a Pathology PDF slip, or click one of the **Quick Test Presets** in the sidebar to run an instant demonstration.")
