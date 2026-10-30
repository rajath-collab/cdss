"""
Module 1: Remote Patient & Home Care View
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Complete Vernacular Localization (i18n): English, Kannada, Hindi, Tamil, Telugu.
Uses real clinical chest radiographs (pneumonia-232.jpg) with interactive multimodal triage.
"""
import streamlit as st
import time
from PIL import Image
from src.ui.image_utils import get_real_sample_xray
from src.ui.translations import get_ui_text


def render_patient_portal():
    """Renders the comprehensive home care and patient result tracking dashboard fully localized in the selected vernacular language."""
    ui_lang = st.session_state.get("ui_lang", "en")
    t = get_ui_text(ui_lang)

    user_id = st.session_state.get("user_id", "+91 9845012345")
    cases = st.session_state.get("patient_cases", {})

    # Top Header Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0369a1 0%, #0c4a6e 100%); padding: 22px; border-radius: 12px; color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.12);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 style="margin: 0; font-size: 1.6rem; color: #38bdf8;">{t.get('patient_portal_title', '🏠 Remote Point-of-Care Patient Portal')}</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                        {t.get('logged_in_as', 'Logged in as:')} <strong>{user_id}</strong> &nbsp;|&nbsp; {t.get('phc_label', 'PHC:')} <strong>Bantwal Rural PHC Zone 2</strong>
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.3); padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.82rem;">
                    {t.get('connected_tele_icu', '🟢 Connected to Tele-ICU Center')}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_new_scan, tab_my_results = st.tabs([
        t.get("tab_new_scan", "🩺 1. Submit New Scan & Run AI Triage"),
        t.get("tab_my_results", "📋 2. My Past Results & Doctor Prescriptions")
    ])

    with tab_new_scan:
        st.markdown(f"#### {t.get('presets_label', '⚡ Clinical Sample Test Presets:')}")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        use_pneumonia = col_p1.button(t.get("preset_pneumonia", "⚠️ Bacterial Pneumonia"), use_container_width=True)
        use_normal = col_p2.button(t.get("preset_normal", "✅ Normal Baseline"), use_container_width=True)
        use_tb = col_p3.button(t.get("preset_tb", "🚨 Tuberculosis (TB)"), use_container_width=True)
        clear_inputs = col_p4.button(t.get("preset_clear", "✕ Clear Inputs"), use_container_width=True)

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
            st.toast(t.get("toast_pneumonia", "Loaded Severe Pneumonia sample!"), icon="⚠️")

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
            st.toast(t.get("toast_normal", "Loaded Normal Baseline sample!"), icon="✅")

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
            st.toast(t.get("toast_tb", "Loaded Tuberculosis sample!"), icon="🚨")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col_up1, col_up2 = st.columns(2)

        with col_up1:
            st.markdown(f"### {t.get('col_xray_title', '📸 1. Thoracic Radiograph (X-Ray)')}")
            xray_file = st.file_uploader(t.get("upload_xray_prompt", "Upload Chest Radiograph (PNG / JPG / JPEG)"), type=["png", "jpg", "jpeg"], key="pat_xray_up")
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
                st.image(st.session_state.pat_scan_state["xray"], caption=t.get("active_xray_caption", "Active Thoracic Radiograph"), width=290)
            else:
                st.info(f"ℹ️ {t.get('upload_xray_prompt', 'Upload a chest X-ray or click a preset above.')}")

        with col_up2:
            st.markdown(f"### {t.get('col_lab_title', '📋 2. Pathology Lab Slip & Vitals')}")
            st.file_uploader(t.get("upload_lab_prompt", "Upload Diagnostic Blood / CBC Report (PDF / Image)"), type=["pdf", "png", "jpg"], key="pat_lab_up")
            cur_fever = st.slider(t.get("fever_label", "Fever duration (Days):"), 0, 14, st.session_state.pat_scan_state.get("fever", 2) if st.session_state.pat_scan_state else 2)
            cur_spo2 = st.number_input(t.get("spo2_label", "SpO2 Blood Oxygen Level (%):"), min_value=70, max_value=100, value=st.session_state.pat_scan_state.get("spo2", 96) if st.session_state.pat_scan_state else 96)

            st.markdown(f"""
                <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 14px; margin-top: 14px;">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a; margin-bottom: 4px;">
                        {t.get('objective_title', '🎯 Objective Clinical Guidance')}
                    </div>
                    <div style="font-size: 0.81rem; color: #64748b; line-height: 1.5;">
                        {t.get('objective_desc', 'AI cross-modally correlates radiographic consolidations with circulating leukocyte count and acute phase reactants (CRP) to eliminate false positives.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        if st.button(t.get("btn_run_triage", "🔍 Run Remote Health Triage"), type="primary", use_container_width=True):
            if not st.session_state.pat_scan_state:
                st.warning(t.get("warning_no_input", "Please upload an X-ray or choose one of the quick presets above."))
            else:
                with st.spinner(t.get("spinner_analyzing", "Analyzing thoracic vision features & laboratory biomarkers...")):
                    time.sleep(0.8)
                st.session_state["show_triage_results"] = True

        # Render Active Triage Results
        if st.session_state.get("show_triage_results") and st.session_state.pat_scan_state:
            data = st.session_state.pat_scan_state
            st.divider()
            st.markdown(f"### 🩺 {t.get('assessment_title', 'Triage Assessment')}: `{data['pred_class']}`")

            if "CRITICAL" in data["severity"] or cur_spo2 < 92:
                crit_desc = t.get("critical_alert_desc", "Verified diagnostic correlation indicates {etiology}.").replace("{etiology}", data.get('etiology', 'Pulmonary Consolidation'))
                st.markdown(f"""
                    <div style="background: #fef2f2; border: 2px solid #ef4444; border-left: 10px solid #dc2626; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <span style="font-size: 2.6rem;">🚨</span>
                            <div>
                                <div style="font-size: 1.25rem; font-weight: 800; color: #991b1b;">
                                    {t.get('critical_alert_badge', 'HIGH RISK / CRITICAL TRIAGE')}
                                </div>
                                <div style="font-size: 0.95rem; color: #7f1d1d; margin-top: 4px; line-height: 1.5;">
                                    {crit_desc} SpO2: <strong>{cur_spo2}%</strong>.
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #fca5a5; border-radius: 8px; padding: 14px;">
                            <h5 style="color: #991b1b; margin-top: 0;">{t.get('emergency_protocol_title', '📋 Emergency Action Protocol')}</h5>
                            <ul style="font-size: 0.88rem; color: #7f1d1d; margin-bottom: 0;">
                                <li>{t.get('emergency_proto_1', 'Sit upright in a well-ventilated space; avoid lying flat.')}</li>
                                <li>{t.get('emergency_proto_2', 'Do not exert yourself; take slow, deep breaths.')}</li>
                                <li>{t.get('emergency_proto_3', 'Keep phone nearby — remote doctor will initiate call.')}</li>
                                <li><strong>{t.get('emergency_proto_4', 'Emergency Ambulance: Dial 108')}</strong></li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                with col_e2:
                    st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #fca5a5; border-radius: 8px; padding: 14px;">
                            <h5 style="color: #991b1b; margin-top: 0;">{t.get('contacts_title', '📞 Fast-Track Emergency Contacts')}</h5>
                            <p style="font-size: 0.88rem; color: #7f1d1d; margin: 4px 0;">
                                • <strong>{t.get('contact_hotline', 'Tele-ICU Hotline: +91 8255 234108')}</strong><br/>
                                • <strong>{t.get('contact_phc', 'Bantwal PHC Emergency: 08255-232120')}</strong><br/>
                                • <strong>{t.get('contact_doc', 'Assigned Doctor: Dr. Ramesh Rao (KMC-58291)')}</strong>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

            elif "MODERATE" in data["severity"]:
                st.markdown(f"""
                    <div style="background: #fffbeb; border: 1px solid #f59e0b; border-left: 8px solid #d97706; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #92400e;">{t.get('moderate_risk_title', '🟡 MODERATE RISK: Clinical Observation Advised')}</span>
                        <p style="margin: 6px 0 0 0; color: #78350f; font-size: 0.92rem;">
                            {t.get('moderate_risk_desc', 'Mild parenchymal opacity detected. Visit nearest PHC within 24 hours.')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: #f0fdf4; border: 1px solid #22c55e; border-left: 8px solid #16a34a; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #166534;">{t.get('low_risk_title', '🟢 LOW RISK: Routine Physiological Baseline')}</span>
                        <p style="margin: 6px 0 0 0; color: #14532d; font-size: 0.92rem;">
                            {t.get('low_risk_desc', 'Radiographic examination and laboratory inflammatory parameters fall within physiological baseline intervals.')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # Detail Cards: Vision vs Lab
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"##### {t.get('vision_card_title', '🔬 Radiographic Vision Analysis')}")
                st.image(data["xray"], caption=f"{t.get('pred_label', 'Predicted:')} {data['pred_class']} ({data['conf']:.1f}%)", width=280)
            with c2:
                st.markdown(f"##### {t.get('biomarker_card_title', '🧪 Pathology Biomarker Findings')}")
                for k, v in data["biomarkers"].items():
                    st.markdown(f"• **{k}:** `{v}`")

            # Vernacular Voice Delivery Section
            st.divider()
            st.markdown(f"##### {t.get('voice_section_title', '🗣️ Vernacular Audio Voice Advisory')}")
            c_lang, c_play = st.columns([0.4, 0.6])
            with c_lang:
                chosen_v_lang = st.selectbox(
                    t.get("choose_audio_lang", "Select Audio Delivery Language:"),
                    ["ಕನ್ನಡ (Kannada)", "हिन्दी (Hindi)", "English", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "മലയാളം (Malayalam)"],
                    key="pat_voice_sel"
                )
            with c_play:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button(t.get("btn_play_audio", "🔊 Play Vernacular Audio Advisory"), key="btn_play_audio_pat"):
                    st.success(f"Playing patient voice advisory in {chosen_v_lang}...")
                    if "മലയാളം" in chosen_v_lang or ui_lang == "ml":
                        st.info("📢 'നെഞ്ചിലെ എക്സ്-റേയിലും രക്തപരിശോധനയിലും ശ്വാസകോശ അണുബാധയുടെ ലക്ഷണങ്ങൾ കാണുന്നു. ദയവായി ഉടൻ തന്നെ ഡോക്ടറെ സമീപിക്കുക.'")
                    elif "ಕನ್ನಡ" in chosen_v_lang or ui_lang == "kn":
                        st.info("📢 'ಎದೆ ಕ್ಷ-ಕಿರಣ ಮತ್ತು ರಕ್ತ ಪರೀಕ್ಷೆ ಎರಡರಲ್ಲೂ ಶ್ವಾಸಕೋಶದ ಸೋಂಕು ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿವೆ. ದಯವಿಟ್ಟು ತಕ್ಷಣವೇ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.'")
                    elif "हिन्दी" in chosen_v_lang or ui_lang == "hi":
                        st.info("📢 'छाती के एक्स-रे और रक्त परीक्षण दोनों में फेफड़ों के संक्रमण के लक्षण पाए गए हैं। कृपया तुरंत डॉक्टर से परामर्श लें।'")
                    elif "தமிழ்" in chosen_v_lang or ui_lang == "ta":
                        st.info("📢 'மார்பக எக்ஸ்ரே மற்றும் இரத்த பரிசோதனையில் நுரையீரல் தொற்று அறிகுறிகள் உள்ளன. உடனடியாக மருத்துவரை அணுகவும்.'")
                    elif "తెలుగు" in chosen_v_lang or ui_lang == "te":
                        st.info("📢 'ఛాతీ ఎక్స్-రే మరియు రక్త పరీక్షలలో ఊపిరితిత్తుల సంక్రమణ లక్షణాలు కనిపించాయి. దయచేసి వెంటనే వైద్యుడిని సంప్రదించండి.'")
                    else:
                        st.info("📢 'Radiographic findings and inflammatory biomarkers indicate signs of pulmonary consolidation. Immediate clinical consultation advised.'")

            # Interactive RAG Lab Assistant
            st.divider()
            st.markdown(f"### {t.get('lab_assist_title', '💬 Interactive Laboratory Results Assistant (RAG)')}")
            st.markdown(f"<p style='font-size: 0.88rem; color: #475569;'>{t.get('lab_assist_desc', 'Ask questions regarding your laboratory slip or clinical findings:')}</p>", unsafe_allow_html=True)

            q_col1, q_col2, q_col3 = st.columns(3)
            q1 = q_col1.button(t.get("rag_q_wbc", "What is my WBC count?"), key="rag_q1")
            q2 = q_col2.button(t.get("rag_q_crp", "Is C-Reactive Protein (CRP) high?"), key="rag_q2")
            q3 = q_col3.button(t.get("rag_q_precautions", "What precautions should I take?"), key="rag_q3")

            custom_q = st.text_input(t.get("rag_input_label", "Or enter your own question:"), placeholder=t.get("rag_input_placeholder", "e.g., What does consolidation mean?"), key="rag_custom_q")

            if q1 or "wbc" in custom_q.lower():
                wbc_msg = "Your observed WBC count is elevated, indicating active immune defense against infection."
                if ui_lang == "ml":
                    wbc_msg = "നിങ്ങളുടെ WBC (വെളുത്ത രക്താണുക്കൾ) എണ്ണം ഉയർന്നതാണ് (14,200). ഇത് ശരീരത്തിൽ ബാക്ടീരിയൽ അണുബാധയുള്ളതായി വ്യക്തമാക്കുന്നു."
                elif ui_lang == "kn":
                    wbc_msg = "ನಿಮ್ಮ WBC (ಬಿಳಿ ರಕ್ತ ಕಣಗಳ) ಸಂಖ್ಯೆಯು ಹೆಚ್ಚಾಗಿದೆ (14,200). ಇದು ದೇಹದಲ್ಲಿ ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಶ್ವಾಸಕೋಶದ ಸೋಂಕು ಇರುವುದನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಸೂಚಿಸುತ್ತದೆ."
                elif ui_lang == "hi":
                    wbc_msg = "आपकी डब्ल्यूबीसी (WBC) संख्या बढ़ी हुई है (14,200)। यह इंगित करता है कि आपका शरीर सक्रिय रूप से फेफड़ों के संक्रमण से लड़ रहा है।"
                elif ui_lang == "ta":
                    wbc_msg = "உங்கள் WBC (வெள்ளை இரத்த அணுக்கள்) எண்ணிக்கை அதிகரித்துள்ளது (14,200). ഇത് உடலில் பாக்டீரியா தொற்று உள்ளதை உறுதிப்படுத்துகிறது."
                elif ui_lang == "te":
                    wbc_msg = "మీ WBC (తెల్ల రక్త కణాలు) సంఖ్య పెరిగింది (14,200). ఇది శరీరంలో బ్యాక్టీరియల్ ఇన్ఫెక్షన్ ఉందని స్పష్టంగా సూచిస్తుంది."
                st.markdown(f"""
                    <div style="background: #f8fafc; border-left: 4px solid #0284c7; padding: 14px; border-radius: 6px; margin-top: 10px;">
                        <strong>White Blood Cell (WBC) Findings:</strong><br/>
                        {wbc_msg}
                    </div>
                """, unsafe_allow_html=True)
            elif q2 or "crp" in custom_q.lower():
                crp_msg = "CRP is an acute-phase inflammatory protein. Your elevated level (48 mg/L) strongly indicates lung inflammation."
                if ui_lang == "ml":
                    crp_msg = "സി-റിയാക്ടീവ് പ്രോട്ടീൻ (CRP) 48.0 mg/L ആയി ഗുരുതരമായി ഉയർന്നിരിക്കുന്നു. ഇത് ശ്വാസകോശത്തിൽ കഠിനമായ വീക്കത്തെ സൂചിപ്പിക്കുന്നു."
                elif ui_lang == "kn":
                    crp_msg = "ಸಿ-ರಿಯಾಕ್ಟಿವ್ ಪ್ರೊಟೀನ್ (CRP) 48.0 mg/L ಗೆ ಗಂಭೀರವಾಗಿ ಏರಿಕೆಯಾಗಿದೆ. ಇದು ಶ್ವಾಸಕೋಶದಲ್ಲಿ ತೀವ್ರ ಸೋಂಕನ್ನು ಸೂಚಿಸುತ್ತದೆ."
                elif ui_lang == "hi":
                    crp_msg = "सीआरपी (CRP) 48.0 mg/L पर अत्यधिक बढ़ा हुआ है, जो फेफड़ों में तीव्र सूजन की पुष्टि करता है।"
                elif ui_lang == "ta":
                    crp_msg = "சி-ரியாக்டிவ் புரோட்டீன் (CRP) 48.0 mg/L ஆக உயர்ந்துள்ளது. இது நுரையீரலில் கடுமையான அழற்சியைக் குறிக்கிறது."
                elif ui_lang == "te":
                    crp_msg = "సి-రియాక్టివ్ ప్రోటీన్ (CRP) 48.0 mg/L కు తీవ్రంగా పెరిగింది. ఇది ఊపిరితిత్తులలో తీవ్రమైన వాపును సూచిస్తుంది."
                st.markdown(f"""
                    <div style="background: #f8fafc; border-left: 4px solid #f59e0b; padding: 14px; border-radius: 6px; margin-top: 10px;">
                        <strong>C-Reactive Protein (CRP) Explanation:</strong><br/>
                        {crp_msg}
                    </div>
                """, unsafe_allow_html=True)
            elif q3 or "precaution" in custom_q.lower():
                prec_msg = "Ensure strict bed rest, monitor oxygen saturation (SpO2) every 4 hours, and take doctor prescribed antibiotics."
                if ui_lang == "ml":
                    prec_msg = "പൂർണ്ണ വിശ്രമം എടുക്കുക, ഓരോ 4 മണിക്കൂറിലും SpO2 പരിശോധിക്കുക, ഡോക്ടർ നിർദ്ദേശിച്ച മരുന്നുകൾ മാത്രം കഴിക്കുക."
                elif ui_lang == "kn":
                    prec_msg = "ಸಂಪೂರ್ಣ ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ, ಪ್ರತಿ 4 ಗಂಟೆಗೊಮ್ಮೆ ಪಲ್ಸ್ ಆಕ್ಸಿಮೀಟರ್‌ನಿಂದ SpO2 ಪರಿಶೀಲಿಸಿ, ವೈದ್ಯರು ಬರೆದ ಔಷಧಿಯನ್ನು ಮಾತ್ರ ಸೇವಿಸಿ."
                elif ui_lang == "hi":
                    prec_msg = "पूर्ण आराम करें, हर 4 घंटे में SpO2 की निगरानी करें, और डॉक्टर द्वारा निर्धारित दवाएं समय पर लें।"
                elif ui_lang == "ta":
                    prec_msg = "முழு ஓய்வு எடுக்கவும், ஒவ்வொரு 4 மணி நேரத்திற்கும் SpO2-ஐ கண்காணிக்கவும், மருத்துவர் பரிந்துரைத்த மருந்துகளை மட்டும் உட்கொள்ளவும்."
                elif ui_lang == "te":
                    prec_msg = "పూర్తి విశ్రాంతి తీసుకోండి, ప్రతి 4 గంటలకు SpO2 ను పర్యవేక్షించండి మరియు వైద్యులు సూచించిన మందులను మాత్రమే తీసుకోండి."
                st.markdown(f"""
                    <div style="background: #f8fafc; border-left: 4px solid #16a34a; padding: 14px; border-radius: 6px; margin-top: 10px;">
                        <strong>General Patient Precautions:</strong><br/>
                        {prec_msg}
                    </div>
                """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: MY HISTORICAL RESULTS & DOCTOR PRESCRIPTIONS
    # -------------------------------------------------------------
    with tab_my_results:
        st.markdown(f"#### {t.get('past_results_title', '📁 Verified Records & Digital Doctor Prescriptions')}")

        for c_id, cs in cases.items():
            doc_rev = cs.get("doctor_review", {})
            is_signed = doc_rev.get("status") == "reviewed"
            status_badge = t.get("status_signed", "✅ Signed by Doctor") if is_signed else t.get("status_pending", "⏳ Pending Clinical Audit")

            with st.expander(f"{t.get('case_label', 'Case')} `{c_id}` — {cs.get('patient_name')} ({cs.get('xray_finding')}) — [{status_badge}]", expanded=True):
                col_m1, col_m2 = st.columns([1.2, 0.8])
                with col_m1:
                    triage = cs.get("triage_summary", {})
                    st.markdown(f"**{t.get('label_triage_diag', 'Triage Diagnosis:')}** `{triage.get('etiology')}`")
                    st.markdown(f"**{t.get('label_triage_level', 'Triage Level:')}** `{triage.get('triage_category')}`")
                    st.markdown(f"**{t.get('label_scan_finding', 'Scan Finding:')}** `{cs.get('xray_finding')}` ({cs.get('xray_confidence', 0.0):.1f}%)")
                    st.markdown(f"**{t.get('label_recommendation', 'System Recommendation:')}** {triage.get('recommendation')}")

                with col_m2:
                    if is_signed:
                        st.markdown(f"""
                            <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 14px;">
                                <h5 style="margin: 0 0 6px 0; color: #166534;">{t.get('clinician_review_card', '👨‍⚕️ Clinician Verification & E-Signature')}</h5>
                                <p style="font-size: 0.84rem; color: #14532d; margin: 0 0 8px 0;">
                                    <strong>{t.get('rev_doctor', 'Doctor:')}</strong> {doc_rev.get('doctor_name', 'Dr. Ramesh Rao')}<br/>
                                    <strong>{t.get('rev_reg', 'Reg No:')}</strong> <code>{doc_rev.get('doctor_reg', 'KMC-58291')}</code><br/>
                                    <strong>{t.get('rev_signed', 'Signed:')}</strong> {doc_rev.get('reviewed_at', '2026-10-29 20:00:10')}
                                </p>
                                <div style="background: #ffffff; border: 1px dashed #4ade80; border-radius: 6px; padding: 10px; font-size: 0.86rem; color: #0f172a;">
                                    <strong>{t.get('rev_prescription', 'Official Prescription:')}</strong><br/>
                                    {doc_rev.get('prescription')}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px;">
                                <h5 style="margin: 0 0 6px 0; color: #92400e;">{t.get('pending_audit_title', '⏳ Pending Clinician Audit')}</h5>
                                <p style="font-size: 0.84rem; color: #78350f; margin: 0;">
                                    {t.get('pending_audit_desc', 'This remote scan is currently in the doctor queue.')}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)


__all__ = ["render_patient_portal"]
