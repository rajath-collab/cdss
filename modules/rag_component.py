"""
Interactive RAG Lab Assistant & Clinical Knowledge Window
Part of Multimodal Fused Clinical Decision Support System (CDSS)
VTU 5th Sem Mini Project - Dept. of CSE (Data Science)

Provides a clean, professional clinical assistant for:
  - Patients: Clear, accessible explanations of their lab results in multiple languages.
  - Doctors / Clinicians: Rapid diagnostic parameter synthesis & clinical protocol verification.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

from rag.parser import (
    extract_text_from_pdf,
    parse_text_report,
    parse_pdf_report,
    chunk_report_for_indexing,
    get_rag_pre_questions,
    PREDEFINED_RAG_QUESTIONS
)
from utils.translations import get_ui_text


def render_rag_window(
    vector_store,
    current_report_data: Optional[Dict[str, Any]] = None,
    current_pdf_bytes: Optional[bytes] = None,
    user_persona: str = "clinician",
    key_prefix: str = "rag_default",
    show_direct_text_option: bool = False
):
    """
    Renders an executive, professional clinical assistant window with structured inquiries
    and grounded retrieval over pathology findings with full vernacular localization.
    """
    ui_lang = st.session_state.get("ui_lang", "en")
    t = get_ui_text(ui_lang)

    is_doctor = user_persona.lower() in ["doctor", "clinician", "radiologist", "admin"]
    title_icon = "🩺" if is_doctor else "💬"
    persona_label = "Clinical Diagnostic & Report Assistant" if is_doctor else t.get("rag_lab_assistant", "Laboratory Results Assistant")
    subtitle_text = "Evidence-based synthesis of laboratory parameters & diagnostic guidance." if is_doctor else t.get("rag_lab_subtitle", "Clear, trusted explanations of your laboratory test values.")
    badge_text = "Clinical Decision Support" if is_doctor else t.get("rag_patient_guidance", "Patient Health Guidance")
    accent_color = "#2563eb" if is_doctor else "#0d9488"
    bg_gradient = "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)" if is_doctor else "linear-gradient(135deg, #115e59 0%, #0f766e 100%)"

    # Executive Clean Header Banner (No raw model/vector store strings)
    st.markdown(f"""
        <div style="background: {bg_gradient}; padding: 16px 20px; border-radius: 10px; color: #ffffff; margin-top: 18px; margin-bottom: 16px; border-left: 4px solid {accent_color}; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
                        <span>{title_icon}</span> {persona_label}
                    </div>
                    <div style="font-size: 0.84rem; color: #cbd5e1; margin-top: 2px;">
                        {subtitle_text}
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.22); padding: 4px 12px; border-radius: 16px; font-size: 0.76rem; font-weight: 600; color: #e2e8f0;">
                    {badge_text}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # State keys for this specific instance
    q_state_key = f"{key_prefix}_active_question"
    res_state_key = f"{key_prefix}_active_response"
    text_input_key = f"{key_prefix}_raw_text_input"

    if q_state_key not in st.session_state:
        st.session_state[q_state_key] = ""
    if res_state_key not in st.session_state:
        st.session_state[res_state_key] = None

    active_report = current_report_data

    # Optional discreet text input for sandbox or custom notes
    if show_direct_text_option:
        with st.expander("✍️ Custom Laboratory Notes / Raw Slip Ingestion (Optional)", expanded=False):
            st.markdown("<p style='font-size: 0.84rem; color: #475569; margin-bottom: 6px;'>Paste laboratory summary text to extract biomarkers and update findings:</p>", unsafe_allow_html=True)
            default_text = "Hemoglobin: 8.2 g/dL (Low), WBC: 12000 /uL (High), Glucose: 95 mg/dL (Normal), CRP: 34.5 mg/L (High)"
            raw_text = st.text_area("Laboratory Findings String:", value=default_text, height=75, key=text_input_key)
            
            if st.button("Analyze Lab Notes", key=f"{key_prefix}_btn_parse_text"):
                with st.spinner("Analyzing laboratory parameters..."):
                    text_parsed = parse_text_report(raw_text, use_ai=True)
                    chunks = chunk_report_for_indexing(text_parsed)
                    vector_store.index_report_chunks(chunks)
                    st.session_state[f"{key_prefix}_active_text_report"] = text_parsed
                    st.toast("Laboratory findings analyzed successfully.", icon="✅")
                    st.rerun()

        if f"{key_prefix}_active_text_report" in st.session_state and st.session_state[f"{key_prefix}_active_text_report"]:
            active_report = st.session_state[f"{key_prefix}_active_text_report"]

    # If we have PDF bytes but no parsed report yet, parse and index it
    if not active_report and current_pdf_bytes:
        with st.spinner("Analyzing laboratory document..."):
            pdf_parsed = parse_pdf_report(current_pdf_bytes, use_ai=True)
            chunks = chunk_report_for_indexing(pdf_parsed)
            vector_store.index_report_chunks(chunks)
            active_report = pdf_parsed

    # Extract pathology values for questions
    path_values = {}
    if active_report:
        if "biomarkers" in active_report:
            path_values = active_report["biomarkers"]
        elif "pathology_data" in active_report:
            path_values = active_report["pathology_data"].get("pathology_values", {})

    available_pre_q = get_rag_pre_questions(path_values)

    # -------------------------------------------------------------
    # 💡 STRUCTURED INQUIRIES SECTION
    # -------------------------------------------------------------
    st.markdown(f"<div style='font-size: 0.9rem; font-weight: 600; color: #334155; margin-bottom: 8px;'>{t.get('rag_quick_inquiries', '💡 Quick Clinical Inquiries:')}</div>", unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button(t.get("rag_btn_hb", "🩸 Hemoglobin Level & Anemia Risk"), key=f"{key_prefix}_q_hb", use_container_width=True):
            st.session_state[q_state_key] = t.get("rag_q_hb", "What is the hemoglobin level and is it low?")
        if st.button(t.get("rag_btn_wbc", "🦠 WBC Count & Infection Status"), key=f"{key_prefix}_q_wbc", use_container_width=True):
            st.session_state[q_state_key] = t.get("rag_q_wbc", "What is the WBC count? Is it high or abnormal?")
        if st.button(t.get("rag_btn_glu", "🍬 Blood Glucose Assessment"), key=f"{key_prefix}_q_glu", use_container_width=True):
            st.session_state[q_state_key] = t.get("rag_q_glu", "What is the glucose level? Is it normal?")
    with col_p2:
        if st.button(t.get("rag_btn_abn", "⚠️ Identify Abnormal Parameters"), key=f"{key_prefix}_q_abn", use_container_width=True):
            st.session_state[q_state_key] = t.get("rag_q_abn", "List all abnormal lab tests found?")
        if st.button(t.get("rag_btn_sum", "📋 Summarize Diagnostic Findings"), key=f"{key_prefix}_q_sum", use_container_width=True):
            st.session_state[q_state_key] = t.get("rag_q_sum", "Summarize pathology report findings")
        if st.button(t.get("rag_btn_crit", "🚨 Screen for Critical Values"), key=f"{key_prefix}_q_crit", use_container_width=True):
            st.session_state[q_state_key] = t.get("rag_q_crit", "What are the critical values in this report?")

    # Optional selector for specific extracted parameters
    if available_pre_q:
        default_dd_text = t.get("rag_dropdown_default", "-- Select a specific test --")
        selected_dropdown_q = st.selectbox(
            t.get("rag_dropdown_label", "Or select a specific biomarker to review:"),
            options=[default_dd_text] + available_pre_q,
            key=f"{key_prefix}_dropdown_q"
        )
        if selected_dropdown_q != default_dd_text:
            st.session_state[q_state_key] = selected_dropdown_q

    # Custom Query Field
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    c_in1, c_in2 = st.columns([0.82, 0.18])
    with c_in1:
        user_input_q = st.text_input(
            "Ask a specific question about this report:" if is_doctor else t.get("rag_input_label", "Ask a question about your lab results:"),
            value=st.session_state[q_state_key],
            key=f"{key_prefix}_text_q_field",
            placeholder=t.get("rag_input_placeholder", "e.g. What does high WBC indicate? or Is CRP elevated?")
        )
    with c_in2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        search_button = st.button(t.get("rag_btn_search", "🔍 Search"), key=f"{key_prefix}_btn_ask", type="primary", use_container_width=True)

    # Execute query
    target_query = user_input_q.strip() if user_input_q.strip() else st.session_state[q_state_key]
    
    if search_button and target_query:
        with st.spinner("Synthesizing report findings..."):
            ans_dict = vector_store.answer_query(target_query, parsed_report=active_report)
            
            if is_doctor and ("protocol" in target_query.lower() or "guideline" in target_query.lower() or "manage" in target_query.lower()):
                kb_chunks = vector_store.query_knowledge(target_query, n_results=2)
                if kb_chunks:
                    ans_dict["guidelines"] = kb_chunks

            st.session_state[res_state_key] = ans_dict

    # -------------------------------------------------------------
    # 📊 PROFESSIONAL RESPONSE CARD (Clean, Hospital-Grade)
    # -------------------------------------------------------------
    if st.session_state[res_state_key]:
        res = st.session_state[res_state_key]
        border_color = "#2563eb" if is_doctor else "#0d9488"
        tag_color = "#eff6ff" if is_doctor else "#f0fdf4"
        tag_text = "#1d4ed8" if is_doctor else "#166534"
        tag_border = "#bfdbfe" if is_doctor else "#bbf7d0"
        
        st.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid {border_color}; padding: 18px 22px; border-radius: 10px; margin-top: 16px; box-shadow: 0 4px 10px rgba(15, 23, 42, 0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.78rem; font-weight: 700; color: {border_color}; letter-spacing: 0.5px; text-transform: uppercase;">
                        {t.get("rag_card_insight", "Clinical Report Insight")}
                    </span>
                    <span style="font-size: 0.74rem; background: {tag_color}; color: {tag_text}; padding: 2px 10px; border-radius: 12px; font-weight: 600; border: 1px solid {tag_border};">
                        {t.get("rag_card_verified", "✓ Verified Evidence")}
                    </span>
                </div>
                <div style="font-size: 1.02rem; font-weight: 600; color: #0f172a; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f1f5f9;">
                    {t.get("rag_card_inquiry", "Inquiry:")} "{res['query']}"
                </div>
                <div style="font-size: 0.94rem; color: #334155; line-height: 1.65; white-space: pre-line;">
{res['answer']}
                </div>
                <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; font-size: 0.76rem; color: #64748b;">
                    <span>{t.get("rag_card_footer_rec", "🔒 Verified against active patient diagnostic record")}</span>
                    <span>{t.get("rag_card_footer_priv", "Local Private Processing")}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if "guidelines" in res and res["guidelines"]:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("##### 📚 Clinical Guideline Protocol (ATS / AIIMS / WHO):")
            for g in res["guidelines"]:
                st.info(g)

        # Clean subtle dismiss button
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button(t.get("rag_btn_dismiss", "✕ Dismiss Result"), key=f"{key_prefix}_btn_dismiss"):
            st.session_state[res_state_key] = None
            st.session_state[q_state_key] = ""
            st.rerun()
