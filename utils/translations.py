"""
utils/translations.py
Comprehensive Vernacular Localization (i18n) Engine for CDSS.
Provides full multi-lingual UI coverage for English, Kannada, Hindi, Tamil, and Telugu.
Ensures identical clinical information, statutory governance, RAG inquiries, and actionable triage.
"""

from typing import Dict, Any

LANGUAGES = {
    "en": {"name": "English", "native": "English", "flag": "🇬🇧"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ (Kannada)", "flag": "🇮🇳"},
    "hi": {"name": "Hindi", "native": "हिन्दी (Hindi)", "flag": "🇮🇳"},
    "ta": {"name": "Tamil", "native": "தமிழ் (Tamil)", "flag": "🇮🇳"},
    "te": {"name": "Telugu", "native": "తెలుగు (Telugu)", "flag": "🇮🇳"},
}

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "en": {
        # Statutory Notice
        "notice_badge": "💡 Assistive Technology Notice",
        "notice_protocol": "Point-of-Care Second Opinion Protocol",
        "notice_main": "This platform serves as a point-of-care second opinion. Final clinical diagnosis rests strictly with certified medical practitioners.",
        "notice_gov_header": "⚖️ Standard Clinical Governance Guidelines & Statutory Regulatory Framework:",
        "notice_aiims": "• AIIMS Clinical AI Standards: Machine inference operates solely as a non-autonomous triage screening aid. Visual activations and lab vectors cannot substitute for bedside auscultation and clinical judgment.",
        "notice_icmr": "• ICMR Ethical Guidelines 2023: Strict doctor-in-the-loop oversight, non-maleficence, bias mitigation, and verified algorithmic transparency via Grad-CAM saliency heatmaps.",
        "notice_nmc": "• National Medical Commission (NMC) Act 2019: Prescriptions, diagnostic finality, and therapeutic directives remain the exclusive legal prerogative of a licensed Registered Medical Practitioner (RMP).",
        "notice_cdsco": "• CDSCO / SaMD Class B: Categorized as a non-invasive Software as a Medical Device (SaMD) clinical decision support aid for diagnostic prioritization.",
        "notice_caption": "ℹ️ Clinical notice is displayed first per AIIMS/ICMR compliance. Click 'Acknowledge & Hide' to maximize screen space.",
        "btn_ack_hide": "👁️ Acknowledge & Hide Notice",
        "btn_show_notice": "💡 Show Assistive Notice",
        
        # App Header
        "app_title": "🩺 Multimodal Fused Clinical Decision Support System (CDSS)",
        "app_subtitle": "Explainable Point-of-Care Thoracic Radiography Vision & Biomarker RAG Triage Platform",
        "app_edition": "Clinical Triage Edition v2.0",
        
        # Sidebar
        "active_session": "Active Session:",
        "role_patient": "🏠 Patient",
        "role_doctor": "👨‍⚕️ Clinician",
        "role_asha": "🤝 ASHA Worker",
        "btn_sign_out": "🚪 Sign Out",
        "select_persona": "Select User Persona / View:",
        "sidebar_disclaimer_title": "💡 Assistive Second Opinion:",
        "sidebar_disclaimer_desc": "Final clinical diagnosis rests strictly with certified medical practitioners.",
        
        # Patient Portal Header
        "patient_portal_title": "🏠 Remote Patient & Home Care Portal",
        "logged_in_as": "Logged in as:",
        "patient_id_label": "ID:",
        "phc_label": "PHC:",
        "connected_tele_icu": "🟢 Connected to Tele-ICU Doctor Network",
        "lang_selector_label": "🌐 Portal Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        
        # Tabs
        "tab_new_scan": "🩺 1. Submit New Scan & Run AI Triage",
        "tab_my_results": "📋 2. My Past Results & Doctor Prescriptions",
        
        # Presets
        "presets_label": "💡 Quick Demo Presets (Select to test automatically):",
        "preset_pneumonia": "🦠 Demo: Severe Pneumonia",
        "preset_normal": "🫁 Demo: Normal Baseline",
        "preset_tb": "🔬 Demo: Suspected TB",
        "preset_clear": "🔄 Clear Inputs",
        "toast_pneumonia": "Loaded Severe Bacterial Pneumonia sample (Scan + Lab)!",
        "toast_normal": "Loaded Healthy Normal Baseline sample (Scan + Lab)!",
        "toast_tb": "Loaded Tuberculosis Suspect sample (Scan + Lab)!",
        
        # Uploads
        "upload_section_title": "📤 Upload Medical Data & Symptoms for Remote Analysis",
        "col_xray_title": "📸 1. Chest Radiograph",
        "upload_xray_prompt": "Snap or upload X-ray photo (PNG / JPEG)",
        "active_xray_caption": "Active Chest Radiograph",
        "col_lab_title": "📋 2. Pathology Lab Slip (PDF)",
        "upload_lab_prompt": "Upload Blood/CBC report (PDF)",
        "objective_title": "🎯 Objective Evidence-Based Ingestion:",
        "objective_desc": "Parameters are extracted strictly from your uploaded laboratory report (WBC, CRP, ESR, Neutrophils, Lymphocytes) via local zero-hallucination PyMuPDF parsing and ChromaDB RAG. Zero subjective guesses or manual approximations.",
        
        # Run Button
        "btn_run_triage": "🔍 Run Remote Health Triage & Alert Doctor",
        "warning_no_input": "Please upload a Chest X-ray, a Lab Slip PDF, or select one of the Quick Demo Presets above.",
        "spinner_analyzing": "Analyzing Thoracic Vision (ResNet-50) & Pathology Biomarkers (RAG)...",
        
        # Triage Results
        "assessment_title": "📊 Immediate Triage Assessment",
        "case_label": "Case",
        
        # Critical Alert
        "critical_alert_badge": "🔴 CRITICAL TRIAGE ALERT: IMMEDIATE DOCTOR NOTIFICATION DISPATCHED",
        "critical_alert_desc": "Verified diagnostic correlation indicates {etiology}. An emergency notification has been transmitted to on-duty Doctor Dr. Ramesh Rao at Bantwal District Hospital.",
        "emergency_protocol_title": "🚑 Emergency Action Protocol:",
        "emergency_proto_1": "Sit upright in a well-ventilated space; avoid lying flat.",
        "emergency_proto_2": "Do not exert yourself; take slow, deep breaths.",
        "emergency_proto_3": "Keep phone nearby — remote doctor will initiate audio call.",
        "emergency_proto_4": "Emergency Ambulance: Dial 108",
        "contacts_title": "📞 Fast-Track Emergency Contacts:",
        "contact_hotline": "Tele-ICU Hotline: +91 8255 234108",
        "contact_phc": "Bantwal PHC Emergency: 08255-232120",
        "contact_doc": "Assigned Doctor: Dr. Ramesh Rao (KMC-58291)",
        
        # Moderate & Low Risk
        "moderate_risk_title": "🟡 MODERATE RISK: Focal Infiltration / Mild Symptoms",
        "moderate_risk_desc": "Findings require routine clinical observation. Visit your nearest Primary Health Centre (PHC) within 24 hours. Your scan has been queued for doctor e-signature.",
        "low_risk_title": "🟢 LOW RISK: Normal Respiratory Baseline",
        "low_risk_desc": "Clear thoracic fields and normal biomarkers. Continue routine outpatient care and hydration.",
        
        # Findings Cards
        "vision_card_title": "🫁 ResNet-50 Radiograph Scan",
        "vision_no_img": "No chest X-ray uploaded.",
        "biomarker_card_title": "🧪 Biomarker Summary",
        "biomarker_no_slip": "No lab slip uploaded.",
        "pred_label": "Prediction:",
        
        # Voice Section
        "voice_section_title": "🎙️ Listen to Triage Advice in Your Language (ಧ್ವನಿ ಸೂಚನೆಗಳು)",
        "choose_audio_lang": "Audio Voice Language:",
        "btn_play_audio": "🔊 Play Vernacular Audio Advisory",
        "spinner_voice": "Generating voice advisory...",
        
        # Interactive Lab Assistant
        "lab_assist_title": "💬 Interactive Laboratory Assistant",
        "lab_assist_desc": "Ask questions about your laboratory values, check if your hemoglobin or WBC count is abnormal, or explore test meanings.",
        
        # Tab 2: Past Results
        "past_results_title": "📬 Your Verified Tele-Consultation Results & Doctor Prescriptions",
        "no_cases_yet": "No scans on record yet. Complete your first scan in Tab 1!",
        "status_signed": "✅ Doctor Signed",
        "status_pending": "⏳ Pending Doctor Review",
        "label_triage_diag": "Triage Diagnosis:",
        "label_triage_level": "Triage Level:",
        "label_scan_finding": "Scan Finding:",
        "label_biomarkers_eval": "Biomarkers Evaluated:",
        "label_recommendation": "System Recommendation:",
        "clinician_review_card": "🩺 Official Clinician Review",
        "rev_doctor": "Doctor:",
        "rev_reg": "Reg No:",
        "rev_signed": "Signed:",
        "rev_prescription": "Prescription / Directive:",
        "pending_audit_title": "⏳ Pending Doctor Audit",
        "pending_audit_desc": "Your AI scan has been queued into the Tele-ICU Cockpit. Doctor review and signed prescription will appear here once verified.",
        
        # Footer & DPDP Policies
        "footer_assistive_title": "Assistive Technology Notice & Clinical Policy",
        "footer_dpdp_title": "Privacy Policy & Data Protection (DPDP Act 2023)",
        "footer_dpdp_cloud": "• Zero Persistent Cloud Storage: In strict compliance with India's Digital Personal Data Protection (DPDP) Act 2023 and HIPAA Security Rules (45 CFR §164), radiographs and laboratory reports are processed ephemerally in local volatile memory.",
        "footer_dpdp_phi": "• Protected Health Information (PHI) Isolation: Patient identifiers are sanitized in-flight; no clinical records or biometric imaging tensors are archived or transmitted across public networks.",
        "footer_dpdp_chroma": "• Local ChromaDB Sandbox: Clinical guideline vectors are maintained locally on-premise without third-party telemetric leakage.",
        "footer_caption": "ℹ️ Click 'Acknowledge & Hide Policies' to collapse clinical notice and privacy cards.",
        "footer_btn_hide": "👁️ Acknowledge & Hide Policies",
        "footer_btn_show": "💡 Show Policy Cards",
        "footer_ack_tag": "🛡️ Statutory Clinical & DPDP Privacy Policies Acknowledged (Zero Cloud Persistence • AIIMS/ICMR/HIPAA Compliant)",
        "footer_expander_title": "📜 Read Full Privacy Policy & Statutory Regulatory Documentation (AIIMS, ICMR, NMC, DPDP Act 2023)",
        "footer_copyright": "© 2026 Multimodal CDSS Triage Platform | Assistive Point-of-Care Edition",
        "footer_statutory_standards": "Statutory Standards: AIIMS Clinical AI • ICMR Ethics 2023 • NMC Act 2019 • DPDP Act 2023 • HIPAA Security Rule • CDSCO SaMD Class B",
        
        # RAG Window
        "rag_lab_assistant": "Laboratory Results Assistant",
        "rag_lab_subtitle": "Clear, trusted explanations of your laboratory test values.",
        "rag_patient_guidance": "Patient Health Guidance",
        "rag_quick_inquiries": "💡 Quick Clinical Inquiries:",
        "rag_btn_hb": "🩸 Hemoglobin Level & Anemia Risk",
        "rag_btn_wbc": "🦠 WBC Count & Infection Status",
        "rag_btn_glu": "🍬 Blood Glucose Assessment",
        "rag_btn_abn": "⚠️ Identify Abnormal Parameters",
        "rag_btn_sum": "📋 Summarize Diagnostic Findings",
        "rag_btn_crit": "🚨 Screen for Critical Values",
        "rag_dropdown_label": "Or select a specific biomarker to review:",
        "rag_dropdown_default": "-- Select a specific test --",
        "rag_input_label": "Ask a question about your lab results:",
        "rag_input_placeholder": "e.g. What does high WBC indicate? or Is CRP elevated?",
        "rag_btn_search": "🔍 Search",
        "rag_card_insight": "Clinical Report Insight",
        "rag_card_verified": "✓ Verified Evidence",
        "rag_card_inquiry": "Inquiry:",
        "rag_card_footer_rec": "🔒 Verified against active patient diagnostic record",
        "rag_card_footer_priv": "Local Private Processing",
        "rag_btn_dismiss": "✕ Dismiss Result",
        "rag_q_hb": "What is the hemoglobin level and is it low?",
        "rag_q_wbc": "What is the WBC count? Is it high or abnormal?",
        "rag_q_glu": "What is the glucose level? Is it normal?",
        "rag_q_abn": "List all abnormal lab tests found?",
        "rag_q_sum": "Summarize pathology report findings",
        "rag_q_crit": "What are the critical values in this report?",
        
        # Biomarkers
        "biomarkers": {
            "wbc": "WBC Count",
            "crp": "C-Reactive Protein (CRP)",
            "esr": "ESR",
            "neutrophils": "Neutrophils",
            "lymphocytes": "Lymphocytes",
            "spo2": "Oxygen Saturation (SpO2)",
            "hemoglobin": "Hemoglobin",
            "platelets": "Platelet Count"
        },
        "statuses": {
            "NORMAL": "NORMAL",
            "HIGH": "HIGH",
            "ELEVATED": "ELEVATED",
            "LOW": "LOW",
            "CRITICAL": "CRITICAL"
        }
    },
    
    "kn": {
        # Statutory Notice
        "notice_badge": "💡 ಸಹಾಯಕ ತಂತ್ರಜ್ಞಾನ ಸೂಚನೆ",
        "notice_protocol": "ಪಾಯಿಂಟ್-ಆಫ್-ಕೇರ್ ದ್ವಿತೀಯ ಅಭಿಪ್ರಾಯ ಪ್ರೋಟೋಕಾಲ್",
        "notice_main": "ಈ ವೇದಿಕೆಯು ಪ್ರಾಥಮಿಕ ಹಂತದ ದ್ವಿತೀಯ ವೈದ್ಯಕೀಯ ಅಭಿಪ್ರಾಯವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ. ಅಂತಿಮ ರೋಗನಿರ್ಣಯವು ಕಡ್ಡಾಯವಾಗಿ ಪ್ರಮಾಣೀಕೃತ ವೈದ್ಯರ ನಿರ್ಧಾರಕ್ಕೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
        "notice_gov_header": "⚖️ ಕ್ಲಿನಿಕಲ್ ನಿಯಮಗಳು ಮತ್ತು ಶಾಸನಬದ್ಧ ನಿಯಂತ್ರಣ ಚೌಕಟ್ಟು:",
        "notice_aiims": "• AIIMS ಕ್ಲಿನಿಕಲ್ AI ಮಾನದಂಡಗಳು: ಯಂತ್ರ ವಿಶ್ಲೇಷಣೆಯು ಕೇವಲ ಸಹಾಯಕ ಸ್ಕ್ರೀನಿಂಗ್ ಸಾಧನವಾಗಿದೆ. ಇದು ವೈದ್ಯರ ನೇರ ಶಾರೀರಿಕ ಪರೀಕ್ಷೆಯನ್ನು ಬದಲಾಯಿಸುವುದಿಲ್ಲ.",
        "notice_icmr": "• ICMR ನೈತಿಕ ಮಾರ್ಗಸೂಚಿಗಳು 2023: ವೈದ್ಯರ ಕಡ್ಡಾಯ ಮೇಲ್ವಿಚಾರಣೆ, ಸುರಕ್ಷತೆ ಮತ್ತು Grad-CAM ಮೂಲಕ ಪಾರದರ್ಶಕತೆ ಖಚಿತಪಡಿಸಲಾಗಿದೆ.",
        "notice_nmc": "• ರಾಷ್ಟ್ರೀಯ ವೈದ್ಯಕೀಯ ಆಯೋಗ (NMC) ಕಾಯ್ದೆ 2019: ಚಿಕಿತ್ಸೆ ಮತ್ತು ಔಷಧ ಚೀಟಿಯನ್ನು ಕೇವಲ ನೋಂದಾಯಿತ ವೈದ್ಯರು (RMP) ಮಾತ್ರ ನೀಡಲು ಕಾನೂನಿನಲ್ಲಿ ಅವಕಾಶವಿದೆ.",
        "notice_cdsco": "• CDSCO / SaMD ವರ್ಗ B: ರೋಗನಿರ್ಣಯ ಆದ್ಯತೀಕರಣಕ್ಕಾಗಿ ಆಕ್ರಮಣಶೀಲವಲ್ಲದ ವೈದ್ಯಕೀಯ ಸಾಧನ ಸಾಫ್ಟ್‌ವೇರ್.",
        "notice_caption": "ℹ️ AIIMS/ICMR ಅನುಸರಣೆಯಂತೆ ಈ ಸೂಚನೆಯನ್ನು ಪ್ರದರ್ಶಿಸಲಾಗಿದೆ. ಮುಚ್ಚಲು 'ಗಮನಿಸಿದ್ದೇನೆ' ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "btn_ack_hide": "👁️ ಗಮನಿಸಿದ್ದೇನೆ - ಸೂಚನೆ ಮುಚ್ಚಿ",
        "btn_show_notice": "💡 ಸಹಾಯಕ ಸೂಚನೆ ತೋರಿಸಿ",
        
        # App Header
        "app_title": "🩺 ಮಲ್ಟಿಮೋಡಲ್ ಕ್ಲಿನಿಕಲ್ ನಿರ್ಧಾರ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆ (CDSS)",
        "app_subtitle": "ಎದೆ ಕ್ಷ-ಕಿರಣ ಮತ್ತು ರಕ್ತ ಪರೀಕ್ಷಾ ವರದಿ ಆಧಾರಿತ AI ಆರೋಗ್ಯ ತಪಾಸಣಾ ವೇದಿಕೆ",
        "app_edition": "ಕ್ಲಿನಿಕಲ್ ಟ್ರಯಾಜ್ ಆವೃತ್ತಿ v2.0",
        
        # Sidebar
        "active_session": "ಸಕ್ರಿಯ ಖಾತೆ:",
        "role_patient": "🏠 ರೋಗಿ (Patient)",
        "role_doctor": "👨‍⚕️ ವೈದ್ಯರು (Clinician)",
        "role_asha": "🤝 ಆಶಾ ಕಾರ್ಯಕರ್ತೆ (ASHA)",
        "btn_sign_out": "🚪 ಹೊರಹೋಗಿ (Sign Out)",
        "select_persona": "ಬಳಕೆದಾರರ ಪಾತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "sidebar_disclaimer_title": "💡 ಸಹಾಯಕ ದ್ವಿತೀಯ ಅಭಿಪ್ರಾಯ:",
        "sidebar_disclaimer_desc": "ಅಂತಿಮ ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಮತ್ತು ಚಿಕಿತ್ಸೆಯು ಕೇವಲ ಪ್ರಮಾಣೀಕೃತ ವೈದ್ಯರ ನಿರ್ಧಾರಕ್ಕೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
        
        # Patient Portal Header
        "patient_portal_title": "🏠 ದೂರಸ್ಥ ರೋಗಿ ಮತ್ತು ಗೃಹ ಆರೈಕೆ ಪೋರ್ಟಲ್",
        "logged_in_as": "ಲಾಗಿನ್ ಆದವರು:",
        "patient_id_label": "ರೋಗಿ ಐಡಿ:",
        "phc_label": "ಆರೋಗ್ಯ ಕೇಂದ್ರ (PHC):",
        "connected_tele_icu": "🟢 ಟೆಲಿ-ಐಸಿಯು ವೈದ್ಯರ ನೆಟ್‌ವರ್ಕ್‌ಗೆ ಸಂಪರ್ಕಗೊಂಡಿದೆ",
        "lang_selector_label": "🌐 ಪೋರ್ಟಲ್ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        
        # Tabs
        "tab_new_scan": "🩺 1. ಹೊಸ ತಪಾಸಣೆ ಮತ್ತು AI ವಿಶ್ಲೇಷಣೆ",
        "tab_my_results": "📋 2. ನನ್ನ ಹಿಂದಿನ ಫಲಿತಾಂಶಗಳು ಮತ್ತು ವೈದ್ಯರ ಚೀಟಿ",
        
        # Presets
        "presets_label": "💡 ತ್ವರಿತ ಡೆಮೊ ಮಾದರಿಗಳು (ಪರೀಕ್ಷಿಸಲು ಯಾವುದಾದರೂ ಒಂದನ್ನು ಆಯ್ಕೆಮಾಡಿ):",
        "preset_pneumonia": "🦠 ಡೆಮೊ: ತೀವ್ರ ನ್ಯುಮೋನಿಯಾ",
        "preset_normal": "🫁 ಡೆಮೊ: ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸ್ಥಿತಿ",
        "preset_tb": "🔬 ಡೆಮೊ: ಸಂಶಯಾಸ್ಪದ ಟಿಬಿ",
        "preset_clear": "🔄 ವಿವರ ತೆರವುಗೊಳಿಸಿ",
        "toast_pneumonia": "ತೀವ್ರ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ನ್ಯುಮೋನಿಯಾ ಮಾದರಿಯನ್ನು ಲೋಡ್ ಮಾಡಲಾಗಿದೆ!",
        "toast_normal": "ಸಾಮಾನ್ಯ ಆರೋಗ್ಯವಂತ ಮಾದರಿಯನ್ನು ಲೋಡ್ ಮಾಡಲಾಗಿದೆ!",
        "toast_tb": "ಕ್ಷಯರೋಗ (ಟಿಬಿ) ಮಾದರಿಯನ್ನು ಲೋಡ್ ಮಾಡಲಾಗಿದೆ!",
        
        # Uploads
        "upload_section_title": "📤 ದೂರಸ್ಥ ತಪಾಸಣೆಗಾಗಿ ವೈದ್ಯಕೀಯ ದಾಖಲೆಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "col_xray_title": "📸 1. ಎದೆ ಕ್ಷ-ಕಿರಣ (Chest X-ray)",
        "upload_xray_prompt": "ಎದೆ ಕ್ಷ-ಕಿರಣ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (PNG / JPEG)",
        "active_xray_caption": "ಪ್ರಸ್ತುತ ಎದೆ ಕ್ಷ-ಕಿರಣ ಚಿತ್ರ",
        "col_lab_title": "📋 2. ರಕ್ತ ಪರೀಕ್ಷಾ ವರದಿ (Lab Slip PDF)",
        "upload_lab_prompt": "ರಕ್ತ / CBC ಪರೀಕ್ಷೆಯ PDF ಸ್ಲಿಪ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "objective_title": "🎯 ಪುರಾವೆ ಆಧಾರಿತ ನೇರ ವಿಶ್ಲೇಷಣೆ:",
        "objective_desc": "ವರದಿಯ ನಿಯತಾಂಕಗಳನ್ನು (WBC, CRP, ESR, ನ್ಯೂಟ್ರೋಫಿಲ್ಸ್) ನಿಮ್ಮ ಅಧಿಕೃತ ಲ್ಯಾಬ್ PDF ನಿಂದ ನೇರವಾಗಿ ಪಡೆಯಲಾಗುತ್ತದೆ. ಯಾವುದೇ ಊಹೆಗಳಿಲ್ಲ, ಸಂಪೂರ್ಣ ಸತ್ಯಾಸತ್ಯತೆ ಖಚಿತ.",
        
        # Run Button
        "btn_run_triage": "🔍 ಆರೋಗ್ಯ ತಪಾಸಣೆ ನಡೆಸಿ ವೈದ್ಯರಿಗೆ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸಿ",
        "warning_no_input": "ದಯವಿಟ್ಟು ಎದೆ ಕ್ಷ-ಕಿರಣ, ರಕ್ತ ಪರೀಕ್ಷಾ PDF ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಮೇಲಿನ ಡೆಮೊ ಬಟನ್‌ಗಳಲ್ಲಿ ಒಂದನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "spinner_analyzing": "ಎದೆ ಕ್ಷ-ಕಿರಣ (ResNet-50) ಮತ್ತು ರಕ್ತ ಪರೀಕ್ಷಾ ವರದಿಯನ್ನು (RAG) ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        
        # Triage Results
        "assessment_title": "📊 ತಕ್ಷಣದ ಆರೋಗ್ಯ ಟ್ರಯಾಜ್ ಮೌಲ್ಯಮಾಪನ",
        "case_label": "ಪ್ರಕರಣ",
        
        # Critical Alert
        "critical_alert_badge": "🔴 ತೀವ್ರ ತುರ್ತು ಎಚ್ಚರಿಕೆ: ವೈದ್ಯರಿಗೆ ತಕ್ಷಣ ತುರ್ತು ಮಾಹಿತಿ ರವಾನಿಸಲಾಗಿದೆ",
        "critical_alert_desc": "ದೃಢೀಕೃತ ತಪಾಸಣೆಯು {etiology} ಸೂಚಿಸುತ್ತದೆ. ಬಂಟ್ವಾಳ ತಾಲೂಕು ಆಸ್ಪತ್ರೆಯ ಡ್ಯೂಟಿ ವೈದ್ಯರಾದ ಡಾ. ರಮೇಶ್ ರಾವ್ ಅವರಿಗೆ ತುರ್ತು ಮಾಹಿತಿ ತಲುಪಿದೆ.",
        "emergency_protocol_title": "🚑 ತುರ್ತು ರೋಗಿ ಮುನ್ನೆಚ್ಚರಿಕೆ ಕ್ರಮಗಳು:",
        "emergency_proto_1": "ಚೆನ್ನಾಗಿ ಗಾಳಿಯಾಡುವ ಕೋಣೆಯಲ್ಲಿ ನೇರವಾಗಿ ಕುಳಿತುಕೊಳ್ಳಿ; ಮಲಗಬೇಡಿ.",
        "emergency_proto_2": "ಹೆಚ್ಚು ಆಯಾಸ ಮಾಡಿಕೊಳ್ಳಬೇಡಿ; ನಿಧಾನವಾಗಿ ಆಳವಾದ ಉಸಿರು ತೆಗೆದುಕೊಳ್ಳಿ.",
        "emergency_proto_3": "ಫೋನ್ ನಿಮ್ಮ ಬಳಿಯೇ ಇಟ್ಟುಕೊಳ್ಳಿ — ಆಸ್ಪತ್ರೆಯ ವೈದ್ಯರು ಕರೆ ಮಾಡುತ್ತಾರೆ.",
        "emergency_proto_4": "ತುರ್ತು ಆಂಬ್ಯುಲೆನ್ಸ್‌ಗಾಗಿ ಡಯಲ್ ಮಾಡಿ: 108",
        "contacts_title": "📞 ತಕ್ಷಣದ ತುರ್ತು ಸಹಾಯವಾಣಿ ಸಂಖ್ಯೆಗಳು:",
        "contact_hotline": "ಟೆಲಿ-ಐಸಿಯು ಸಹಾಯವಾಣಿ: +91 8255 234108",
        "contact_phc": "ಬಂಟ್ವಾಳ ಆಸ್ಪತ್ರೆ ತುರ್ತು ವಿಭಾಗ: 08255-232120",
        "contact_doc": "ನಿಯೋಜಿತ ವೈದ್ಯರು: ಡಾ. ರಮೇಶ್ ರಾವ್ (KMC-58291)",
        
        # Moderate & Low Risk
        "moderate_risk_title": "🟡 ಮಧ್ಯಮ ಅಪಾಯ: ಸೌಮ್ಯ ಸೋಂಕು / ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿವೆ",
        "moderate_risk_desc": "24 ಗಂಟೆಗಳ ಒಳಗೆ ಹತ್ತಿರದ ಪ್ರಾಥಮಿಕ ಆರೋಗ್ಯ ಕೇಂದ್ರಕ್ಕೆ (PHC) ಭೇಟಿ ನೀಡಿ. ನಿಮ್ಮ ವರದಿಯನ್ನು ವೈದ್ಯರ ಪರಿಶೀಲನೆಗೆ ಕಳುಹಿಸಲಾಗಿದೆ.",
        "low_risk_title": "🟢 ಕಡಿಮೆ ಅಪಾಯ: ಸಾಮಾನ್ಯ ಆರೋಗ್ಯಕರ ಶ್ವಾಸಕೋಶ",
        "low_risk_desc": "ಎದೆ ಕ್ಷ-ಕಿರಣ ಮತ್ತು ರಕ್ತ ಪರೀಕ್ಷೆಗಳು ಸಾಮಾನ್ಯ ವ್ಯಾಪ್ತಿಯಲ್ಲಿವೆ. ನಿಯಮಿತ ವಿಶ್ರಾಂತಿ, ಬೆಚ್ಚಗಿನ ನೀರು ಕುಡಿಯುವುದು ಮುಂದುವರಿಸಿ.",
        
        # Findings Cards
        "vision_card_title": "🫁 ResNet-50 ಎದೆ ಕ್ಷ-ಕಿರಣ ಫಲಿತಾಂಶ",
        "vision_no_img": "ಯಾವುದೇ ಎದೆ ಕ್ಷ-ಕಿರಣ ಅಪ್‌ಲೋಡ್ ಮಾಡಲಾಗಿಲ್ಲ.",
        "biomarker_card_title": "🧪 ರಕ್ತ ಪರೀಕ್ಷೆಯ ಪ್ರಮುಖ ನಿಯತಾಂಕಗಳು",
        "biomarker_no_slip": "ಯಾವುದೇ ರಕ್ತ ಪರೀಕ್ಷಾ ವರದಿ ಅಪ್‌ಲೋಡ್ ಮಾಡಲಾಗಿಲ್ಲ.",
        "pred_label": "ಮುನ್ನೋಟ:",
        
        # Voice Section
        "voice_section_title": "🎙️ ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಆರೋಗ್ಯ ಸಲಹೆ ಆಲಿಸಿ (ಧ್ವನಿ ಸೂಚನೆ)",
        "choose_audio_lang": "ಧ್ವನಿ ಭಾಷೆ:",
        "btn_play_audio": "🔊 ಧ್ವನಿ ಸಲಹೆಯನ್ನು ಆಲಿಸಿ (Play Audio)",
        "spinner_voice": "ಧ್ವನಿ ಸಲಹೆಯನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...",
        
        # Interactive Lab Assistant
        "lab_assist_title": "💬 ಸಂವಾದಾತ್ಮಕ ಲ್ಯಾಬ್ ಸಹಾಯಕ (Lab Assistant)",
        "lab_assist_desc": "ನಿಮ್ಮ ರಕ್ತ ಪರೀಕ್ಷೆಗಳ ಬಗ್ಗೆ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ (ಉದಾಹರಣೆಗೆ: ನನ್ನ WBC ಅಥವಾ ಹಿಮೋಗ್ಲೋಬಿನ್ ಸಾಮಾನ್ಯವೇ?)",
        
        # Tab 2: Past Results
        "past_results_title": "📬 ನಿಮ್ಮ ದೃಢೀಕೃತ ಫಲಿತಾಂಶಗಳು ಮತ್ತು ವೈದ್ಯರ ಔಷಧ ಚೀಟಿ",
        "no_cases_yet": "ಇನ್ನೂ ಯಾವುದೇ ತಪಾಸಣೆ ನಡೆದಿಲ್ಲ. ಮೊದಲನೇ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ಹೊಸ ತಪಾಸಣೆ ಮಾಡಿ!",
        "status_signed": "✅ ವೈದ್ಯರಿಂದ ದೃಢೀಕೃತ",
        "status_pending": "⏳ ವೈದ್ಯರ ಪರಿಶೀಲನೆ ಬಾಕಿ ಇದೆ",
        "label_triage_diag": "ಟ್ರಯಾಜ್ ರೋಗನಿರ್ಣಯ:",
        "label_triage_level": "ಅಪಾಯದ ಹಂತ:",
        "label_scan_finding": "ಸ್ಕ್ಯಾನ್ ಫಲಿತಾಂಶ:",
        "label_biomarkers_eval": "ಪರಿಶೀಲಿಸಲಾದ ರಕ್ತ ಪರೀಕ್ಷೆಗಳು:",
        "label_recommendation": "ವ್ಯವಸ್ಥೆಯ ಶಿಫಾರಸು:",
        "clinician_review_card": "🩺 ಅಧಿಕೃತ ವೈದ್ಯರ ತಪಾಸಣಾ ವರದಿ",
        "rev_doctor": "ಪರಿಶೀಲಿಸಿದ ವೈದ್ಯರು:",
        "rev_reg": "ವೈದ್ಯರ ನೋಂದಣಿ ಸಂಖ್ಯೆ:",
        "rev_signed": "ಸಹಿ ಮಾಡಿದ ಸಮಯ:",
        "rev_prescription": "ವೈದ್ಯರ ಔಷಧ ಚೀಟಿ ಮತ್ತು ಸೂಚನೆಗಳು:",
        "pending_audit_title": "⏳ ವೈದ್ಯರ ಪರಿಶೀಲನೆ ಬಾಕಿ ಇದೆ",
        "pending_audit_desc": "ನಿಮ್ಮ ವರದಿಯನ್ನು ಟೆಲಿ-ಐಸಿಯು ತಜ್ಞರಿಗೆ ಕಳುಹಿಸಲಾಗಿದೆ. ವೈದ್ಯರು ಪರಿಶೀಲಿಸಿ ಸಹಿ ಮಾಡಿದ ನಂತರ ಔಷಧ ಚೀಟಿ ಇಲ್ಲಿ ಲಭ್ಯವಾಗುತ್ತದೆ.",
        
        # Footer & DPDP Policies
        "footer_assistive_title": "ಸಹಾಯಕ ತಂತ್ರಜ್ಞಾನ ಸೂಚನೆ ಮತ್ತು ಕ್ಲಿನಿಕಲ್ ನೀತಿ",
        "footer_dpdp_title": "ಗೌಪ್ಯತೆ ನೀತಿ ಮತ್ತು ದತ್ತಾಂಶ ಸಂರಕ್ಷಣೆ (DPDP ಕಾಯ್ದೆ 2023)",
        "footer_dpdp_cloud": "• ಶೂನ್ಯ ಕ್ಲೌಡ್ ಸಂಗ್ರಹಣೆ: ಭಾರತದ ಡಿಜಿಟಲ್ ವೈಯಕ್ತಿಕ ದತ್ತಾಂಶ ಸಂರಕ್ಷಣೆ (DPDP) ಕಾಯ್ದೆ 2023 ಮತ್ತು HIPAA ನಿಯಮಗಳಿಗೆ ಬದ್ಧವಾಗಿ, ಎಕ್ಸ್-ರೇ ಮತ್ತು ಲ್ಯಾಬ್ ವರದಿಗಳನ್ನು ಕೇವಲ ಸ್ಥಳೀಯ ತಾತ್ಕಾಲಿಕ ಮೆಮೊರಿಯಲ್ಲಿ ಸಂಸ್ಕರಿಸಲಾಗುತ್ತದೆ.",
        "footer_dpdp_phi": "• ರೋಗಿಯ ವೈಯಕ್ತಿಕ ಆರೋಗ್ಯ ಮಾಹಿತಿ (PHI) ರಕ್ಷಣೆ: ರೋಗಿಯ ಗುರುತಿನ ವಿವರಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿಡಲಾಗುತ್ತದೆ; ಯಾವುದೇ ಬಯೋಮೆಟ್ರಿಕ್ ಚಿತ್ರಗಳು ಸಾರ್ವಜನಿಕ ನೆಟ್‌ವರ್ಕ್‌ಗಳಲ್ಲಿ ಪ್ರಸಾರವಾಗುವುದಿಲ್ಲ.",
        "footer_dpdp_chroma": "• ಸ್ಥಳೀಯ ChromaDB ಸ್ಯಾಂಡ್‌ಬಾಕ್ಸ್: ಕ್ಲಿನಿಕಲ್ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಹೊರಗಿನ ಸರ್ವರ್‌ಗಳಿಗೆ ಸೋರಿಕೆಯಾಗದಂತೆ ಕೇವಲ ಸ್ಥಳೀಯ ಕಂಪ್ಯೂಟರ್‌ನಲ್ಲಿ ನಿರ್ವಹಿಸಲಾಗುತ್ತದೆ.",
        "footer_caption": "ℹ️ ಕ್ಲಿನಿಕಲ್ ಸೂಚನೆ ಮತ್ತು ಗೌಪ್ಯತಾ ಕಾರ್ಡ್‌ಗಳನ್ನು ಮರೆಮಾಡಲು 'ಗಮನಿಸಿದ್ದೇನೆ' ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "footer_btn_hide": "👁️ ಗಮನಿಸಿದ್ದೇನೆ - ನೀತಿಗಳನ್ನು ಮರೆಮಾಡಿ",
        "footer_btn_show": "💡 ನೀತಿ ಕಾರ್ಡ್‌ಗಳನ್ನು ತೋರಿಸಿ",
        "footer_ack_tag": "🛡️ ಶಾಸನಬದ್ಧ ಕ್ಲಿನಿಕಲ್ ಮತ್ತು DPDP ಗೌಪ್ಯತಾ ನೀತಿಗಳನ್ನು ಗಮನಿಸಲಾಗಿದೆ (ಶೂನ್ಯ ಕ್ಲೌಡ್ ಸಂಗ್ರಹಣೆ • AIIMS/ICMR/HIPAA ಅನುಸರಣೆ)",
        "footer_expander_title": "📜 ಸಂಪೂರ್ಣ ಗೌಪ್ಯತೆ ನೀತಿ ಮತ್ತು ಶಾಸನಬದ್ಧ ನಿಯಂತ್ರಣ ದಾಖಲಾತಿಗಳನ್ನು ಓದಿ (AIIMS, ICMR, NMC, DPDP ಕಾಯ್ದೆ 2023)",
        "footer_copyright": "© 2026 ಮಲ್ಟಿಮೋಡಲ್ CDSS ಟ್ರಯಾಜ್ ವೇದಿಕೆ | ಪಾಯಿಂಟ್-ಆಫ್-ಕೇರ್ ಆವೃತ್ತಿ",
        "footer_statutory_standards": "ಶಾಸನಬದ್ಧ ಮಾನದಂಡಗಳು: AIIMS ಕ್ಲಿನಿಕಲ್ AI • ICMR ನೈತಿಕತೆ 2023 • NMC ಕಾಯ್ದೆ 2019 • DPDP ಕಾಯ್ದೆ 2023 • HIPAA ಸುರಕ್ಷತೆ • CDSCO SaMD ವರ್ಗ B",
        
        # RAG Window
        "rag_lab_assistant": "ಪ್ರಯೋಗಾಲಯ ಫಲಿತಾಂಶಗಳ ಸಹಾಯಕ",
        "rag_lab_subtitle": "ನಿಮ್ಮ ರಕ್ತ ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳ ಸ್ಪಷ್ಟ ಮತ್ತು ವಿಶ್ವಾಸಾರ್ಹ ವಿವರಣೆಗಳು.",
        "rag_patient_guidance": "ರೋಗಿ ಆರೋಗ್ಯ ಮಾರ್ಗದರ್ಶನ",
        "rag_quick_inquiries": "💡 ತ್ವರಿತ ಕ್ಲಿನಿಕಲ್ ಪ್ರಶ್ನೆಗಳು:",
        "rag_btn_hb": "🩸 ಹಿಮೋಗ್ಲೋಬಿನ್ ಮಟ್ಟ ಮತ್ತು ರಕ್ತಹೀನತೆಯ ಅಪಾಯ",
        "rag_btn_wbc": "🦠 ಬಿಳಿ ರಕ್ತ ಕಣಗಳು (WBC) ಮತ್ತು ಸೋಂಕಿನ ಸ್ಥಿತಿ",
        "rag_btn_glu": "🍬 ರಕ್ತದ ಗ್ಲೂಕೋಸ್ / ಸಕ್ಕರೆ ಮಟ್ಟ ತಪಾಸಣೆ",
        "rag_btn_abn": "⚠️ ಅಸಹಜ ರಕ್ತ ಪರೀಕ್ಷೆಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿ",
        "rag_btn_sum": "📋 ಒಟ್ಟಾರೆ ರೋಗನಿರ್ಣಯ ಸಾರಾಂಶ",
        "rag_btn_crit": "🚨 ತುರ್ತು ಮತ್ತು ಗಂಭೀರ ಮೌಲ್ಯಗಳ ಪರಿಶೀಲನೆ",
        "rag_dropdown_label": "ಅಥವಾ ನಿರ್ದಿಷ್ಟ ರಕ್ತ ಪರೀಕ್ಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "rag_dropdown_default": "-- ನಿರ್ದಿಷ್ಟ ಪರೀಕ್ಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ --",
        "rag_input_label": "ನಿಮ್ಮ ಲ್ಯಾಬ್ ವರದಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ:",
        "rag_input_placeholder": "ಉದಾ: ಹೆಚ್ಚಿನ WBC ಏನನ್ನು ಸೂಚಿಸುತ್ತದೆ? ಅಥವಾ CRP ಹೆಚ್ಚಾಗಿದೆಯೇ?",
        "rag_btn_search": "🔍 ಹುಡುಕಿ (Search)",
        "rag_card_insight": "ಕ್ಲಿನಿಕಲ್ ವರದಿ ಒಳನೋಟ",
        "rag_card_verified": "✓ ದೃಢೀಕೃತ ಸಾಕ್ಷ್ಯ",
        "rag_card_inquiry": "ಪ್ರಶ್ನೆ:",
        "rag_card_footer_rec": "🔒 ಸಕ್ರಿಯ ರೋಗಿಯ ವೈದ್ಯಕೀಯ ದಾಖಲೆಗಳ ಆಧಾರದ ಮೇಲೆ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
        "rag_card_footer_priv": "ಸ್ಥಳೀಯ ಖಾಸಗಿ ಸಂಸ್ಕರಣೆ (Zero Cloud Leakage)",
        "rag_btn_dismiss": "✕ ಫಲಿತಾಂಶ ಮುಚ್ಚಿ (Dismiss)",
        "rag_q_hb": "ಹಿಮೋಗ್ಲೋಬಿನ್ ಮಟ್ಟ ಎಷ್ಟು ಮತ್ತು ಅದು ಕಡಿಮೆಯಾಗಿದೆಯೇ?",
        "rag_q_wbc": "WBC ಸಂಖ್ಯೆ ಎಷ್ಟು? ಅದು ಹೆಚ್ಚಾಗಿದೆಯೇ ಅಥವಾ ಅಸಹಜವಾಗಿದೆಯೇ?",
        "rag_q_glu": "ಗ್ಲೂಕೋಸ್ ಮಟ್ಟ ಎಷ್ಟು? ಅದು ಸಾಮಾನ್ಯವೇ?",
        "rag_q_abn": "ವರದಿಯಲ್ಲಿರುವ ಎಲ್ಲಾ ಅಸಹಜ ರಕ್ತ ಪರೀಕ್ಷೆಗಳನ್ನು ಪಟ್ಟಿ ಮಾಡಿ?",
        "rag_q_sum": "ಲ್ಯಾಬ್ ವರದಿಯ ಪ್ರಮುಖ ರೋಗನಿರ್ಣಯ ಸಾರಾಂಶ ತಿಳಿಸಿ",
        "rag_q_crit": "ಈ ವರದಿಯಲ್ಲಿರುವ ಗಂಭೀರ ಅಥವಾ ತುರ್ತು ಮೌಲ್ಯಗಳು ಯಾವುವು?",
        
        # Biomarkers
        "biomarkers": {
            "wbc": "ಬಿಳಿ ರಕ್ತ ಕಣಗಳು (WBC Count)",
            "crp": "ಸಿ-ರಿಯಾಕ್ಟಿವ್ ಪ್ರೋಟೀನ್ (CRP)",
            "esr": "ಇಎಸ್ಆರ್ (ESR)",
            "neutrophils": "ನ್ಯೂಟ್ರೋಫಿಲ್ಗಳು (Neutrophils)",
            "lymphocytes": "ಲಿಂಫೋಸೈಟ್ಗಳು (Lymphocytes)",
            "spo2": "ಆಮ್ಲಜನಕ ಮಟ್ಟ (SpO2)",
            "hemoglobin": "ಹಿಮೋಗ್ಲೋಬಿನ್ (Hemoglobin)",
            "platelets": "ಪ್ಲೇಟ್ಲೆಟ್ಗಳು (Platelets)"
        },
        "statuses": {
            "NORMAL": "ಸಾಮಾನ್ಯ (Normal)",
            "HIGH": "ಹೆಚ್ಚಾಗಿದೆ (High)",
            "ELEVATED": "ಏರಿಕೆಯಾಗಿದೆ (Elevated)",
            "LOW": "ಕಡಿಮೆಯಾಗಿದೆ (Low)",
            "CRITICAL": "ತುರ್ತು (Critical)"
        }
    },

    "hi": {
        # Statutory Notice
        "notice_badge": "💡 सहायक प्रौद्योगिकी सूचना",
        "notice_protocol": "पॉइंट-ऑफ-केयर द्वितीय राय प्रोटोकॉल",
        "notice_main": "यह प्रणाली पॉइंट-ऑफ-केयर द्वितीय राय के रूप में कार्य करती है। अंतिम नैदानिक ​​निर्णय केवल प्रमाणित चिकित्सा चिकित्सकों के पास है।",
        "notice_gov_header": "⚖️ मानक नैदानिक ​​दिशा-निर्देश और वैधानिक विनियामक ढांचा:",
        "notice_aiims": "• AIIMS क्लिनिकल AI मानक: मशीन का निष्कर्ष केवल एक गैर-स्वायत्त स्क्रीनिंग सहायता है। यह डॉक्टर की प्रत्यक्ष जांच का विकल्प नहीं हो सकता।",
        "notice_icmr": "• ICMR नैतिक दिशानिर्देश 2023: डॉक्टर की अनिवार्य निगरानी, सुरक्षा और Grad-CAM के माध्यम से पारदर्शिता सुनिश्चित की गई है।",
        "notice_nmc": "• राष्ट्रीय चिकित्सा आयोग (NMC) अधिनियम 2019: नुस्खा (प्रिस्क्रिप्शन) और अंतिम निदान केवल पंजीकृत चिकित्सक (RMP) का कानूनी विशेषाधिकार है।",
        "notice_cdsco": "• CDSCO / SaMD वर्ग B: नैदानिक ​​प्राथमिकता के लिए गैर-इनवेसिव सॉफ्टवेयर एज़ अ मेडिकल डिवाइस (SaMD) सहायता।",
        "notice_caption": "ℹ️ AIIMS/ICMR अनुपालन के अनुसार सूचना प्रदर्शित है। स्क्रीन स्पेस बढ़ाने के लिए 'स्वीकार करें' पर क्लिक करें।",
        "btn_ack_hide": "👁️ स्वीकार करें और सूचना छिपाएं",
        "btn_show_notice": "💡 सहायक सूचना दिखाएं",
        
        # App Header
        "app_title": "🩺 मल्टीमॉडल फ़्यूज्ड क्लिनिकल डिसीजन सपोर्ट सिस्टम (CDSS)",
        "app_subtitle": "छाती के एक्स-रे और रक्त परीक्षण पर आधारित व्याख्यात्मक AI ट्राइएज प्लेटफॉर्म",
        "app_edition": "क्लिनिकल ट्राइएज संस्करण v2.0",
        
        # Sidebar
        "active_session": "सक्रिय सत्र:",
        "role_patient": "🏠 मरीज (Patient)",
        "role_doctor": "👨‍⚕️ डॉक्टर (Clinician)",
        "role_asha": "🤝 आशा कार्यकर्ता (ASHA)",
        "btn_sign_out": "🚪 साइन आउट (Sign Out)",
        "select_persona": "उपयोगकर्ता भूमिका चुनें:",
        "sidebar_disclaimer_title": "💡 सहायक द्वितीय राय:",
        "sidebar_disclaimer_desc": "अंतिम नैदानिक ​​निदान और उपचार पूरी तरह से प्रमाणित डॉक्टरों के अधीन है।",
        
        # Patient Portal Header
        "patient_portal_title": "🏠 रिमोट मरीज और घरेलू देखभाल पोर्टल",
        "logged_in_as": "लॉग इन किया गया:",
        "patient_id_label": "मरीज आईडी:",
        "phc_label": "स्वास्थ्य केंद्र (PHC):",
        "connected_tele_icu": "🟢 टेली-आईसीयू डॉक्टर नेटवर्क से कनेक्टेड",
        "lang_selector_label": "🌐 पोर्टल की भाषा चुनें / Choose Language:",
        
        # Tabs
        "tab_new_scan": "🩺 1. नई जांच जमा करें और AI विश्लेषण करें",
        "tab_my_results": "📋 2. मेरे पिछले परिणाम और डॉक्टर का पर्चा",
        
        # Presets
        "presets_label": "💡 त्वरित डेमो नमूने (स्वचालित परीक्षण के लिए चुनें):",
        "preset_pneumonia": "🦠 डेमो: गंभीर निमोनिया",
        "preset_normal": "🫁 डेमो: सामान्य स्वास्थ्य स्थिति",
        "preset_tb": "🔬 डेमो: संदिग्ध टीबी (Tuberculosis)",
        "preset_clear": "🔄 इनपुट साफ़ करें",
        "toast_pneumonia": "गंभीर निमोनिया का नमूना लोड किया गया!",
        "toast_normal": "सामान्य स्वस्थ नमूना लोड किया गया!",
        "toast_tb": "टीबी संदिग्ध नमूना लोड किया गया!",
        
        # Uploads
        "upload_section_title": "📤 रिमोट विश्लेषण के लिए मेडिकल डेटा अपलोड करें",
        "col_xray_title": "📸 1. छाती का एक्स-रे (Chest X-ray)",
        "upload_xray_prompt": "एक्स-रे फोटो अपलोड करें (PNG / JPEG)",
        "active_xray_caption": "सक्रिय छाती का एक्स-रे",
        "col_lab_title": "📋 2. पैथोलॉजी लैब पर्ची (PDF)",
        "upload_lab_prompt": "रक्त / CBC रिपोर्ट की PDF अपलोड करें",
        "objective_title": "🎯 साक्ष्य-आधारित प्रत्यक्ष विश्लेषण:",
        "objective_desc": "पैरामीटर (WBC, CRP, ESR, न्यूट्रोफिल) सीधे आपकी लैब रिपोर्ट से सुरक्षित रूप से निकाले जाते हैं। कोई अनुमान नहीं, 100% सटीकता।",
        
        # Run Button
        "btn_run_triage": "🔍 स्वास्थ्य ट्राइएज चलाएं और डॉक्टर को सूचित करें",
        "warning_no_input": "कृपया छाती का एक्स-रे, लैब पर्ची अपलोड करें या ऊपर दिए गए डेमो बटन में से चुनें।",
        "spinner_analyzing": "एक्स-रे (ResNet-50) और रक्त रिपोर्ट (RAG) का विश्लेषण किया जा रहा है...",
        
        # Triage Results
        "assessment_title": "📊 तत्काल ट्राइएज स्वास्थ्य मूल्यांकन",
        "case_label": "केस",
        
        # Critical Alert
        "critical_alert_badge": "🔴 गंभीर आपातकालीन अलर्ट: डॉक्टर को तुरंत सूचना भेजी गई",
        "critical_alert_desc": "नैदानिक ​​पुष्टि {etiology} की ओर संकेत करती है। बंटवाल अस्पताल के ड्यूटी डॉक्टर डॉ. रमेश राव को तत्काल सूचना प्रेषित कर दी गई है।",
        "emergency_protocol_title": "🚑 आपातकालीन सावधानियां और प्रोटोकॉल:",
        "emergency_proto_1": "हवादार कमरे में सीधे बैठें; सपाट न लेटें।",
        "emergency_proto_2": "ज्यादा मेहनत न करें; धीरे-धीरे गहरी सांसें लें।",
        "emergency_proto_3": "फोन पास रखें — अस्पताल के डॉक्टर जल्द कॉल करेंगे।",
        "emergency_proto_4": "आपातकालीन एम्बुलेंस: डायल करें 108",
        "contacts_title": "📞 तत्काल आपातकालीन संपर्क सूत्र:",
        "contact_hotline": "टेली-आईसीयू हेल्पलाइन: +91 8255 234108",
        "contact_phc": "बंटवाल आपातकालीन केंद्र: 08255-232120",
        "contact_doc": "निर्दिष्ट चिकित्सक: डॉ. रमेश राव (KMC-58291)",
        
        # Moderate & Low Risk
        "moderate_risk_title": "🟡 मध्यम जोखिम: हल्का संक्रमण या फेफड़ों में धब्बा",
        "moderate_risk_desc": "24 घंटे के भीतर नजदीकी प्राथमिक स्वास्थ्य केंद्र (PHC) जाएं। आपकी जांच डॉक्टर के सत्यापन के लिए भेज दी गई है।",
        "low_risk_title": "🟢 कम जोखिम: सामान्य श्वसन प्रणाली",
        "low_risk_desc": "छाती का एक्स-रे और रक्त परीक्षण सामान्य हैं। पर्याप्त पानी पिएं और सामान्य देखभाल जारी रखें।",
        
        # Findings Cards
        "vision_card_title": "🫁 ResNet-50 एक्स-रे विश्लेषण",
        "vision_no_img": "कोई एक्स-रे अपलोड नहीं किया गया।",
        "biomarker_card_title": "🧪 बायोमार्कर और रक्त परीक्षण सारांश",
        "biomarker_no_slip": "कोई लैब पर्ची अपलोड नहीं की गई।",
        "pred_label": "अनुमान:",
        
        # Voice Section
        "voice_section_title": "🎙️ अपनी भाषा में स्वास्थ्य सलाह सुनें (ध्वनि परामर्श)",
        "choose_audio_lang": "ऑडियो भाषा चुनें:",
        "btn_play_audio": "🔊 ध्वनि सलाह सुनें (Play Audio)",
        "spinner_voice": "ध्वनि तैयार की जा रही है...",
        
        # Interactive Lab Assistant
        "lab_assist_title": "💬 इंटरएक्टिव लैब सहायक (Lab Assistant)",
        "lab_assist_desc": "अपनी लैब रिपोर्ट के बारे में सवाल पूछें (जैसे: क्या मेरा WBC या हीमोग्लोबिन सामान्य है?)",
        
        # Tab 2: Past Results
        "past_results_title": "📬 आपके सत्यापित परिणाम और डॉक्टर का नुस्खा",
        "no_cases_yet": "अभी तक कोई रिकॉर्ड नहीं है। पहले टैब में नई जांच करें!",
        "status_signed": "✅ डॉक्टर द्वारा सत्यापित",
        "status_pending": "⏳ डॉक्टर की समीक्षा लंबित",
        "label_triage_diag": "ट्राइएज निदान:",
        "label_triage_level": "जोखिम स्तर:",
        "label_scan_finding": "स्कैन निष्कर्ष:",
        "label_biomarkers_eval": "मूल्यांकित बायोमार्कर:",
        "label_recommendation": "प्रणाली की सिफारिश:",
        "clinician_review_card": "🩺 आधिकारिक चिकित्सक समीक्षा",
        "rev_doctor": "डॉक्टर:",
        "rev_reg": "पंजीकरण संख्या:",
        "rev_signed": "हस्ताक्षर समय:",
        "rev_prescription": "डॉक्टर का पर्चा और दवाइयां:",
        "pending_audit_title": "⏳ डॉक्टर की समीक्षा प्रतीक्षित है",
        "pending_audit_desc": "आपकी जांच टेली-आईसीयू में भेज दी गई है। डॉक्टर द्वारा सत्यापित होने के बाद हस्ताक्षरित नुस्खा यहाँ दिखाई देगा।",
        
        # Footer & DPDP Policies
        "footer_assistive_title": "सहायक प्रौद्योगिकी सूचना और क्लिनिकल नीति",
        "footer_dpdp_title": "गोपनीयता नीति और डेटा संरक्षण (DPDP अधिनियम 2023)",
        "footer_dpdp_cloud": "• शून्य क्लाउड स्टोरेज: भारत के डिजिटल व्यक्तिगत डेटा संरक्षण (DPDP) अधिनियम 2023 और HIPAA सुरक्षा नियमों (45 CFR §164) के पूर्ण अनुपालन में, एक्स-रे और लैब रिपोर्ट केवल स्थानीय मेमोरी में संसाधित की जाती हैं।",
        "footer_dpdp_phi": "• संरक्षित स्वास्थ्य सूचना (PHI) सुरक्षा: मरीज की पहचान सुरक्षित रखी जाती है; कोई भी बायोमेट्रिक डेटा सार्वजनिक नेटवर्क पर प्रसारित नहीं किया जाता।",
        "footer_dpdp_chroma": "• स्थानीय ChromaDB सैंडबॉक्स: क्लिनिकल दिशा-निर्देश स्थानीय रूप से सुरक्षित रखे जाते हैं बिना किसी डेटा रिसाव के।",
        "footer_caption": "ℹ️ क्लिनिकल नोटिस और गोपनीयता कार्ड छिपाने के लिए 'स्वीकार करें' पर क्लिक करें।",
        "footer_btn_hide": "👁️ स्वीकार करें और नीतियां छिपाएं",
        "footer_btn_show": "💡 नीति कार्ड दिखाएं",
        "footer_ack_tag": "🛡️ वैधानिक क्लिनिकल और DPDP गोपनीयता नीतियां स्वीकृत (शून्य क्लाउड संग्रहण • AIIMS/ICMR/HIPAA अनुपालन)",
        "footer_expander_title": "📜 पूरी गोपनीयता नीति और वैधानिक नियामक दस्तावेज पढ़ें (AIIMS, ICMR, NMC, DPDP अधिनियम 2023)",
        "footer_copyright": "© 2026 मल्टीमॉडल CDSS ट्राइएज प्लेटफॉर्म | पॉइंट-ऑफ-केयर संस्करण",
        "footer_statutory_standards": "वैधानिक मानक: AIIMS क्लिनिकल AI • ICMR नैतिकता 2023 • NMC अधिनियम 2019 • DPDP अधिनियम 2023 • HIPAA सुरक्षा नियम • CDSCO SaMD क्लास B",
        
        # RAG Window
        "rag_lab_assistant": "प्रयोगशाला परिणाम सहायक (Lab Assistant)",
        "rag_lab_subtitle": "आपके प्रयोगशाला परीक्षण परिणामों की स्पष्ट और विश्वसनीय व्याख्या।",
        "rag_patient_guidance": "मरीज स्वास्थ्य मार्गदर्शन",
        "rag_quick_inquiries": "💡 त्वरित क्लिनिकल प्रश्न:",
        "rag_btn_hb": "🩸 हीमोग्लोबिन स्तर और एनीमिया जोखिम",
        "rag_btn_wbc": "🦠 श्वेत रक्त कोशिकाएं (WBC) और संक्रमण स्थिति",
        "rag_btn_glu": "🍬 ब्लड ग्लूकोज / शुगर मूल्यांकन",
        "rag_btn_abn": "⚠️ असामान्य पैरामीटर पहचानें",
        "rag_btn_sum": "📋 डायग्नोस्टिक निष्कर्ष सारांश",
        "rag_btn_crit": "🚨 गंभीर और आपातकालीन मानों की जांच",
        "rag_dropdown_label": "या समीक्षा के लिए एक विशिष्ट टेस्ट चुनें:",
        "rag_dropdown_default": "-- एक विशिष्ट टेस्ट चुनें --",
        "rag_input_label": "अपनी लैब रिपोर्ट के बारे में एक प्रश्न पूछें:",
        "rag_input_placeholder": "उदा. उच्च WBC क्या दर्शाता है? या क्या CRP बढ़ा हुआ है?",
        "rag_btn_search": "🔍 खोजें (Search)",
        "rag_card_insight": "क्लिनिकल रिपोर्ट इनसाइट",
        "rag_card_verified": "✓ सत्यापित साक्ष्य",
        "rag_card_inquiry": "पूछा गया प्रश्न:",
        "rag_card_footer_rec": "🔒 सक्रिय मरीज मेडिकल रिकॉर्ड के आधार पर सत्यापित",
        "rag_card_footer_priv": "स्थानीय निजी प्रसंस्करण (Zero Cloud Leakage)",
        "rag_btn_dismiss": "✕ परिणाम हटाएं (Dismiss)",
        "rag_q_hb": "हीमोग्लोबिन का स्तर क्या है और क्या यह कम है?",
        "rag_q_wbc": "WBC काउंट क्या है? क्या यह असामान्य या बढ़ा हुआ है?",
        "rag_q_glu": "ग्लूकोज स्तर क्या है? क्या यह सामान्य है?",
        "rag_q_abn": "पाए गए सभी असामान्य लैब परीक्षणों की सूची बनाएं?",
        "rag_q_sum": "पैथोलॉजी रिपोर्ट के मुख्य निष्कर्षों का सारांश दें",
        "rag_q_crit": "इस रिपोर्ट में गंभीर या चिंताजनक मान कौन से हैं?",
        
        # Biomarkers
        "biomarkers": {
            "wbc": "श्वेत रक्त कोशिकाएं (WBC Count)",
            "crp": "सी-रिएक्टिव प्रोटीन (CRP)",
            "esr": "ईएसआर (ESR)",
            "neutrophils": "न्यूट्रोफिल (Neutrophils)",
            "lymphocytes": "लिम्फोसाइट (Lymphocytes)",
            "spo2": "ऑक्सीजन स्तर (SpO2)",
            "hemoglobin": "हीमोग्लोबिन (Hemoglobin)",
            "platelets": "प्लेटलेट्स (Platelets)"
        },
        "statuses": {
            "NORMAL": "सामान्य (Normal)",
            "HIGH": "अधिक (High)",
            "ELEVATED": "बढ़ा हुआ (Elevated)",
            "LOW": "कम (Low)",
            "CRITICAL": "गंभीर (Critical)"
        }
    },

    "ta": {
        # Statutory Notice
        "notice_badge": "💡 உதவி தொழில்நுட்ப அறிவிப்பு",
        "notice_protocol": "பாயிண்ட்-ஆஃப்-கேர் இரண்டாம் நிலை கருத்து நெறிமுறை",
        "notice_main": "இந்த தளம் ஒரு துணை மருத்துவக் கருத்தாக மட்டுமே செயல்படுகிறது. இறுதி நோயறிதல் தகுதிவாய்ந்த மருத்துவரிடம் மட்டுமே உள்ளது.",
        "notice_gov_header": "⚖️ மருத்துவ வழிகாட்டுதல்கள் மற்றும் சட்ட ஒழுங்குமுறை கட்டமைப்பு:",
        "notice_aiims": "• AIIMS கிளினிக்கல் AI தரநிலைகள்: இயந்திர பகுப்பாய்வு ஒரு துணை திரையிடல் கருவி மட்டுமே. இது மருத்துவரின் நேரடி பரிசோதனைக்கு மாற்றாகாது.",
        "notice_icmr": "• ICMR நெறிமுறை வழிகாட்டுதல்கள் 2023: மருத்துவரின் மேற்பார்வை மற்றும் Grad-CAM மூலம் வெளிப்படைத்தன்மை உறுதி செய்யப்பட்டுள்ளது.",
        "notice_nmc": "• தேசிய மருத்துவ ஆணையம் (NMC) சட்டம் 2019: மருந்துகளைப் பரிந்துரைப்பது பதிவுசெய்த மருத்துவ பயிற்சியாளரின் (RMP) பிரத்தியேக உரிமை.",
        "notice_cdsco": "• CDSCO / SaMD வகுப்பு B: ஆக்கிரமிப்பு இல்லாத மருத்துவ சாதன மென்பொருள்.",
        "notice_caption": "ℹ️ AIIMS/ICMR வழிகாட்டுதல்படி அறிவிப்பு காட்டப்பட்டுள்ளது. மறைக்க 'அங்கீகரிக்கவும்' என்பதைக் கிளிக் செய்யவும்.",
        "btn_ack_hide": "👁️ அறிவிப்பை மறைக்கவும்",
        "btn_show_notice": "💡 அறிவிப்பைக் காட்டவும்",
        
        # App Header
        "app_title": "🩺 பல்துறை ஒருங்கிணைந்த மருத்துவ முடிவு ஆதரவு அமைப்பு (CDSS)",
        "app_subtitle": "மார்பு எக்ஸ்ரே மற்றும் இரத்த பரிசோதனை அடிப்படையிலான AI சுகாதார தளம்",
        "app_edition": "மருத்துவ ட்ரையாஜ் பதிப்பு v2.0",
        
        # Sidebar
        "active_session": "செயலில் உள்ள கணக்கு:",
        "role_patient": "🏠 நோயாளி (Patient)",
        "role_doctor": "👨‍⚕️ மருத்துவர் (Clinician)",
        "role_asha": "🤝 ஆஷா பணியாளர் (ASHA)",
        "btn_sign_out": "🚪 வெளியேறு (Sign Out)",
        "select_persona": "பயனர் பாத்திரத்தைத் தேர்ந்தெடுக்கவும்:",
        "sidebar_disclaimer_title": "💡 துணை மருத்துவக் கருத்து:",
        "sidebar_disclaimer_desc": "இறுதி நோயறிதல் மற்றும் சிகிச்சை மருத்துவரின் முடிவிற்கு உட்பட்டது.",
        
        # Patient Portal Header
        "patient_portal_title": "🏠 தொலைதூர நோயாளி மற்றும் வீட்டுப் பராமரிப்பு போர்டல்",
        "logged_in_as": "உள்நுழைந்துள்ளவர்:",
        "patient_id_label": "நோயாளி ஐடி:",
        "phc_label": "ஆரோக்கிய மையம் (PHC):",
        "connected_tele_icu": "🟢 டெலி-ஐசியூ மருத்துவர் நெட்வொர்க்குடன் இணைக்கப்பட்டுள்ளது",
        "lang_selector_label": "🌐 போர்டல் மொழியைத் தேர்ந்தெடுக்கவும்:",
        
        # Tabs
        "tab_new_scan": "🩺 1. புதிய பரிசோதனை மற்றும் AI ஆய்வு",
        "tab_my_results": "📋 2. முந்தைய முடிவுகள் & மருத்துவரின் மருந்துச் சீட்டு",
        
        # Presets
        "presets_label": "💡 விரைவு டெமோ மாதிரிகள் (பரிசோதிக்க தேர்ந்தெடுக்கவும்):",
        "preset_pneumonia": "🦠 டெமோ: தீவிர நிமோனியா",
        "preset_normal": "🫁 டெமோ: சாதாரண நிலை",
        "preset_tb": "🔬 டெமோ: காசநோய் (TB) சந்தேகம்",
        "preset_clear": "🔄 அழிக்கவும்",
        "toast_pneumonia": "தீவிர நிமோனியா மாதிரி ஏற்றப்பட்டது!",
        "toast_normal": "இயல்பான ஆரோக்கிய மாதிரி ஏற்றப்பட்டது!",
        "toast_tb": "காசநோய் மாதிரி ஏற்றப்பட்டது!",
        
        # Uploads
        "upload_section_title": "📤 தொலைதூர பரிசோதனைக்காக மருத்துவ ஆவணங்களைப் பதிவேற்றவும்",
        "col_xray_title": "📸 1. மார்பு எக்ஸ்ரே (Chest X-ray)",
        "upload_xray_prompt": "எக்ஸ்ரே புகைப்படத்தைப் பதிவேற்றவும் (PNG / JPEG)",
        "active_xray_caption": "செயலில் உள்ள எக்ஸ்ரே படம்",
        "col_lab_title": "📋 2. இரத்த பரிசோதனை அறிக்கை (PDF)",
        "upload_lab_prompt": "இரத்த பரிசோதனை PDF சீட்டைப் பதிவேற்றவும்",
        "objective_title": "🎯 சான்று அடிப்படையிலான நேரடிப் பகுப்பாய்வு:",
        "objective_desc": "அளவீடுகள் (WBC, CRP, ESR) உங்கள் அதிகாரப்பூர்வ ஆய்வக அறிக்கையிலிருந்து நேரடியாகப் பெறப்படுகின்றன. எந்த யூகமும் இல்லை.",
        
        # Run Button
        "btn_run_triage": "🔍 பரிசோதனை செய்து மருத்துவருக்கு எச்சரிக்கையனுப்பவும்",
        "warning_no_input": "தயவுசெய்து எக்ஸ்ரே, இரத்த அறிக்கை PDF பதிவேற்றவும் அல்லது டெமோ பட்டனைத் தேர்ந்தெடுக்கவும்.",
        "spinner_analyzing": "எக்ஸ்ரே (ResNet-50) மற்றும் இரத்த அறிக்கையை (RAG) பகுப்பாய்வு செய்கிறது...",
        
        # Triage Results
        "assessment_title": "📊 உடனடி ட்ரையாஜ் சுகாதார மதிப்பீடு",
        "case_label": "வழக்கு",
        
        # Critical Alert
        "critical_alert_badge": "🔴 அவசர எச்சரிக்கை: மருத்துவருக்கு உடனடியாக தகவல் அனுப்பப்பட்டது",
        "critical_alert_desc": "உறுதிப்படுத்தப்பட்ட நோயறிதல் {etiology} ஐக் குறிக்கிறது. பந்த்வால் அரசு மருத்துவமனை டாக்டர் ரமேஷ் ராவ் அவர்களுக்கு அவசர தகவல் அனுப்பப்பட்டுள்ளது.",
        "emergency_protocol_title": "🚑 அவசரகால முன்னெச்சரிக்கை வழிகாட்டுதல்:",
        "emergency_proto_1": "நன்றாகக் காற்றோட்டமான இடத்தில் நிமிர்ந்து உட்காரவும்; படுக்க வேண்டாம்.",
        "emergency_proto_2": "அதிக சிரமப்பட வேண்டாம்; மெதுவாக ஆழ்ந்த மூச்சை எடுக்கவும்.",
        "emergency_proto_3": "தொலைபேசியை அருகில் வைத்திருக்கவும் — மருத்துவர் விரைவில் அழைப்பார்.",
        "emergency_proto_4": "அவசர ஆம்புலன்ஸ்: 108 ஐ அழைக்கவும்",
        "contacts_title": "📞 உடனடி அவசர உதவி எண்கள்:",
        "contact_hotline": "டெலி-ஐசியூ உதவி எண்: +91 8255 234108",
        "contact_phc": "பந்த்வால் மருத்துவமனை அவசரப்பிரிவு: 08255-232120",
        "contact_doc": "நியமிக்கப்பட்ட மருத்துவர்: டாக்டர் ரமேஷ் ராவ் (KMC-58291)",
        
        # Moderate & Low Risk
        "moderate_risk_title": "🟡 மிதமான ஆபத்து: லேசான தொற்று அறிகுறிகள்",
        "moderate_risk_desc": "24 மணி நேரத்திற்குள் ஆரம்ப சுகாதார நிலையத்திற்கு (PHC) செல்லவும். உங்கள் அறிக்கை மருத்துவருக்கு அனுப்பப்பட்டுள்ளது.",
        "low_risk_title": "🟢 குறைந்த ஆபத்து: இயல்பான நுரையீரல் நிலை",
        "low_risk_desc": "எக்ஸ்ரே மற்றும் இரத்த பரிசோதனை முடிவுகள் இயல்பான வரம்பில் உள்ளன. போதுமான ஓய்வு எடுக்கவும்.",
        
        # Findings Cards
        "vision_card_title": "🫁 ResNet-50 எக்ஸ்ரே ஆய்வு",
        "vision_no_img": "எக்ஸ்ரே எதுவும் பதிவேற்றப்படவில்லை.",
        "biomarker_card_title": "🧪 இரத்த பரிசோதனை அளவீடுகள் சுருக்கம்",
        "biomarker_no_slip": "ஆய்வக அறிக்கை எதுவும் பதிவேற்றப்படவில்லை.",
        "pred_label": "கணிப்பு:",
        
        # Voice Section
        "voice_section_title": "🎙️ உங்கள் தாய்மொழியில் மருத்துவ ஆலோசனையைக் கேளுங்கள்",
        "choose_audio_lang": "ஆடியோ மொழி:",
        "btn_play_audio": "🔊 ஆடியோ கேட்கவும் (Play Audio)",
        "spinner_voice": "ஆடியோ தயாராகிறது...",
        
        # Interactive Lab Assistant
        "lab_assist_title": "💬 ஊடாடும் ஆய்வக உதவியாளர் (Lab Assistant)",
        "lab_assist_desc": "உங்கள் இரத்த பரிசோதனை அளவுகள் பற்றி சந்தேகங்களைக் கேளுங்கள்.",
        
        # Tab 2: Past Results
        "past_results_title": "📬 உங்கள் சரிபார்க்கப்பட்ட முடிவுகள் மற்றும் மருந்துச் சீட்டு",
        "no_cases_yet": "பதிவுகள் எதுவும் இல்லை. முதல் தாவலில் புதிய பரிசோதனையைத் தொடங்குங்கள்!",
        "status_signed": "✅ மருத்துவர் கையொப்பமிட்டது",
        "status_pending": "⏳ மருத்துவர் மதிப்பாய்வு நிலுவையில் உள்ளது",
        "label_triage_diag": "ட்ரையாஜ் நோயறிதல்:",
        "label_triage_level": "ஆபத்து நிலை:",
        "label_scan_finding": "ஸ்கேன் முடிவு:",
        "label_biomarkers_eval": "மதிப்பாய்வு செய்யப்பட்ட அளவுகள்:",
        "label_recommendation": "பரிந்துரை:",
        "clinician_review_card": "🩺 அதிகாரப்பூர்வ மருத்துவர் அறிக்கை",
        "rev_doctor": "மருத்துவர்:",
        "rev_reg": "பதிவு எண்:",
        "rev_signed": "கையொப்பமிட்ட நேரம்:",
        "rev_prescription": "மருந்துச் சீட்டு மற்றும் குறிப்புகள்:",
        "pending_audit_title": "⏳ மருத்துவர் சரிபார்ப்பு நிலுவையில் உள்ளது",
        "pending_audit_desc": "உங்கள் பரிசோதனை டெலி-ஐசியூ மருத்துவருக்கு அனுப்பப்பட்டுள்ளது. சரிபார்த்த பிறகு மருந்துச் சீட்டு இங்கு கிடைக்கும்.",
        
        # Footer & DPDP Policies
        "footer_assistive_title": "உதவி தொழில்நுட்ப அறிவிப்பு & மருத்துவக் கொள்கை",
        "footer_dpdp_title": "தனியுரிமைக் கொள்கை & தரவுப் பாதுகாப்பு (DPDP சட்டம் 2023)",
        "footer_dpdp_cloud": "• கிளவுட் சேமிப்பு இல்லை: இந்தியாவின் DPDP சட்டம் 2023 மற்றும் HIPAA பாதுகாப்பு விதிகளின்படி, எக்ஸ்ரே மற்றும் ஆய்வக அறிக்கைகள் உள்ளூர் நினைவகத்தில் மட்டுமே தற்காலிகமாக செயலாக்கப்படுகின்றன.",
        "footer_dpdp_phi": "• நோயாளி தகவல் பாதுகாப்பு: நோயாளியின் அடையாள விவரங்கள் பாதுகாக்கப்படுகின்றன; எந்த பயோமெட்ரிக் படங்களும் பொது நெட்வொர்க்குகளில் பரப்பப்படுவதில்லை.",
        "footer_dpdp_chroma": "• உள்ளூர் ChromaDB சேமிப்பகம்: மருத்துவ வழிகாட்டுதல்கள் மூன்றாம் தரப்பினருக்கு கசியாமல் உள்ளூரில் பராமரிக்கப்படுகின்றன.",
        "footer_caption": "ℹ️ மருத்துவ அறிவிப்பு மற்றும் தனியுரிமை அட்டைகளை மறைக்க 'அங்கீகரிக்கவும்' என்பதைக் கிளிக் செய்யவும்.",
        "footer_btn_hide": "👁️ கொள்கைகளை மறைக்கவும்",
        "footer_btn_show": "💡 கொள்கை அட்டைகளைக் காட்டவும்",
        "footer_ack_tag": "🛡️ மருத்துவ மற்றும் DPDP தனியுரிமைக் கொள்கைகள் அங்கீகரிக்கப்பட்டன (AIIMS/ICMR/HIPAA இணக்கம்)",
        "footer_expander_title": "📜 முழு தனியுரிமைக் கொள்கை மற்றும் ஒழுங்குமுறை ஆவணங்களைப் படிக்கவும் (AIIMS, ICMR, NMC, DPDP சட்டம் 2023)",
        "footer_copyright": "© 2026 CDSS மருத்துவ தளம் | பாயிண்ட்-ஆஃப்-கேர் பதிப்பு",
        "footer_statutory_standards": "சட்டப்பூர்வ தரநிலைகள்: AIIMS கிளினிக்கல் AI • ICMR நெறிமுறைகள் 2023 • NMC சட்டம் 2019 • DPDP சட்டம் 2023 • HIPAA • CDSCO SaMD வகுப்பு B",
        
        # RAG Window
        "rag_lab_assistant": "ஆய்வக முடிவுகள் உதவியாளர்",
        "rag_lab_subtitle": "உங்கள் ஆய்வக சோதனை முடிவுகளின் தெளிவான, நம்பகமான விளக்கங்கள்.",
        "rag_patient_guidance": "நோயாளி சுகாதார வழிகாட்டுதல்",
        "rag_quick_inquiries": "💡 விரைவு மருத்துவக் கேள்விகள்:",
        "rag_btn_hb": "🩸 ஹீமோகுளோபின் அளவு & இரத்த சோகை ஆபத்து",
        "rag_btn_wbc": "🦠 வெள்ளை இரத்த அணுக்கள் (WBC) & தொற்று நிலை",
        "rag_btn_glu": "🍬 இரத்த சர்க்கரை அளவு மதிப்பீடு",
        "rag_btn_abn": "⚠️ அசாதாரண அளவீடுகளைக் கண்டறியவும்",
        "rag_btn_sum": "📋 நோயறிதல் முடிவுகளின் சுருக்கம்",
        "rag_btn_crit": "🚨 அவசர மற்றும் ஆபத்தான அளவீடுகளைச் சரிபார்க்கவும்",
        "rag_dropdown_label": "அல்லது ஒரு குறிப்பிட்ட பரிசோதனையைத் தேர்ந்தெடுக்கவும்:",
        "rag_dropdown_default": "-- குறிப்பிட்ட பரிசோதனையைத் தேர்ந்தெடுக்கவும் --",
        "rag_input_label": "உங்கள் ஆய்வக முடிவுகளைப் பற்றி கேள்வி கேளுங்கள்:",
        "rag_input_placeholder": "எ.கா. அதிக WBC எதைக் குறிக்கிறது? அல்லது CRP அதிகரித்துள்ளதா?",
        "rag_btn_search": "🔍 தேடுங்கள் (Search)",
        "rag_card_insight": "மருத்துவ அறிக்கை நுண்ணறிவு",
        "rag_card_verified": "✓ சரிபார்க்கப்பட்ட சான்று",
        "rag_card_inquiry": "கேள்வி:",
        "rag_card_footer_rec": "🔒 நோயாளியின் அதிகாரப்பூர்வ மருத்துவ பதிவுகளின்படி சரிபார்க்கப்பட்டது",
        "rag_card_footer_priv": "உள்ளூர் தனிப்பட்ட செயலாக்கம் (Local Private Processing)",
        "rag_btn_dismiss": "✕ முடிவை மூடவும் (Dismiss)",
        "rag_q_hb": "ஹீமோகுளோபின் அளவு என்ன, அது குறைவாக உள்ளதா?",
        "rag_q_wbc": "WBC எண்ணிக்கை என்ன? அது அதிகமா அல்லது அசாதாரணமா?",
        "rag_q_glu": "குளுக்கோஸ் அளவு என்ன? அது இயல்பானதா?",
        "rag_q_abn": "அறிக்கையில் உள்ள அசாதாரண சோதனைகளை பட்டியலிடுங்கள்?",
        "rag_q_sum": "ஆய்வக அறிக்கையின் முக்கிய முடிவுகளை சுருக்கமாகக் கூறுங்கள்",
        "rag_q_crit": "இந்த அறிக்கையில் உள்ள முக்கியமான அல்லது அவசர மதிப்புகள் யாவை?",
        
        # Biomarkers
        "biomarkers": {
            "wbc": "வெள்ளை இரத்த அணுக்கள் (WBC Count)",
            "crp": "சி-ரியாக்டிவ் புரோட்டீன் (CRP)",
            "esr": "இ.எஸ்.ஆர் (ESR)",
            "neutrophils": "நியூட்ரோபில்ஸ் (Neutrophils)",
            "lymphocytes": "லிம்போசைட்டுகள் (Lymphocytes)",
            "spo2": "ஆக்சிஜன் அளவு (SpO2)",
            "hemoglobin": "ஹீமோகுளோபின் (Hemoglobin)",
            "platelets": "பிளேட்லெட்டுகள் (Platelets)"
        },
        "statuses": {
            "NORMAL": "சாதாரணமானது (Normal)",
            "HIGH": "அதிகம் (High)",
            "ELEVATED": "அதிகரித்துள்ளது (Elevated)",
            "LOW": "குறைவு (Low)",
            "CRITICAL": "ஆபத்தானது (Critical)"
        }
    },

    "te": {
        # Statutory Notice
        "notice_badge": "💡 సహాయక సాంకేతిక నోటీసు",
        "notice_protocol": "పాయింట్-ఆఫ్-కేర్ సెకండ్ ఒపీనియన్ ప్రోటోకాల్",
        "notice_main": "ఈ వ్యవస్థ ప్రాథమిక దశలో సహాయక వైద్య సలహాగా మాత్రమే పనిచేస్తుంది. తుది రోగనిర్ధారణ సర్టిఫైడ్ వైద్యుల ఆధ్వర్యంలో మాత్రమే జరుగుతుంది.",
        "notice_gov_header": "⚖️ ప్రామాణిక క్లినికల్ మార్గదర్శకాలు & చట్టబద్ధమైన నియంత్రణ వ్యవస్థ:",
        "notice_aiims": "• AIIMS క్లినికల్ AI ప్రమాణాలు: మెషిన్ విశ్లేషణ కేవలం సహాయక స్క్రీనింగ్ సాధనం మాత్రమే. ఇది వైద్యుల ప్రత్యక్ష పరీక్షకు ప్రత్యామ్నాయం కాదు.",
        "notice_icmr": "• ICMR నైతిక మార్గదర్శకాలు 2023: వైద్యుల తప్పనిసరి పర్యవేక్షణ మరియు Grad-CAM ద్వారా పారదర్శకత నిర్ధారించబడింది.",
        "notice_nmc": "• నేషనల్ మెడికల్ కమిషన్ (NMC) చట్టం 2019: మందులు మరియు వైద్య ప్రిస్క్రిప్షన్ కేవలం రిజిస్టర్డ్ మెడికల్ ప్రాక్టీషనర్ (RMP) ద్వారా మాత్రమే ఇవ్వబడుతుంది.",
        "notice_cdsco": "• CDSCO / SaMD క్లాస్ B: నాన్-ఇన్వాసివ్ మెడికల్ డివైస్ సాఫ్ట్‌వేర్ సహాయం.",
        "notice_caption": "ℹ️ AIIMS/ICMR నిబంధనల ప్రకారం నోటీసు ప్రదర్శించబడింది. దాచడానికి 'సరే' క్లిక్ చేయండి.",
        "btn_ack_hide": "👁️ నోటీసును దాచండి",
        "btn_show_notice": "💡 సహాయక నోటీసును చూపించండి",
        
        # App Header
        "app_title": "🩺 మల్టీమోడల్ ఫ్యూజ్డ్ క్లినికల్ డెసిషన్ సపోర్ట్ సిస్టమ్ (CDSS)",
        "app_subtitle": "ఛాతీ ఎక్స్-రే మరియు రక్త పరీక్షల ఆధారిత AI ట్రయాజ్ ప్లాట్‌ఫారమ్",
        "app_edition": "క్లినికల్ ట్రయాజ్ ఎడిషన్ v2.0",
        
        # Sidebar
        "active_session": "సక్రియ సెషన్:",
        "role_patient": "🏠 రోగి (Patient)",
        "role_doctor": "👨‍⚕️ డాక్టర్ (Clinician)",
        "role_asha": "🤝 ఆశా కార్యకర్త (ASHA)",
        "btn_sign_out": "🚪 లాగ్ అవుట్ (Sign Out)",
        "select_persona": "వినియోగదారు పాత్రను ఎంచుకోండి:",
        "sidebar_disclaimer_title": "💡 సహాయక రెండవ అభిప్రాయం:",
        "sidebar_disclaimer_desc": "తుది రోగనిర్ధారణ మరియు చికిత్స సర్టిఫైడ్ వైద్యుల ఆధ్వర్యంలో మాత్రమే జరుగుతుంది.",
        
        # Patient Portal Header
        "patient_portal_title": "🏠 రిమోట్ పేషెంట్ & హోమ్ కేర్ పోర్టల్",
        "logged_in_as": "లాగిన్ అయినవారు:",
        "patient_id_label": "పేషెంట్ ఐడి:",
        "phc_label": "ఆరోగ్య కేంద్రం (PHC):",
        "connected_tele_icu": "🟢 టెలి-ఐసియు డాక్టర్ నెట్‌వర్క్‌కు అనుసంధానించబడింది",
        "lang_selector_label": "🌐 పోర్టల్ భాషను ఎంచుకోండి / Select Language:",
        
        # Tabs
        "tab_new_scan": "🩺 1. కొత్త పరీక్షను సమర్పించండి & AI విశ్లేషణ",
        "tab_my_results": "📋 2. మునుపటి ఫలితాలు & వైద్యుల ప్రిస్క్రిప్షన్",
        
        # Presets
        "presets_label": "💡 శీఘ్ర డెమో నమూనాలు (పరీక్షించడానికి ఎంచుకోండి):",
        "preset_pneumonia": "🦠 డెమో: తీవ్రమైన న్యుమోనియా",
        "preset_normal": "🫁 డెమో: సాధారణ ఆరోగ్య స్థితి",
        "preset_tb": "🔬 డెమో: అనుమానిత క్షయవ్యాధి (TB)",
        "preset_clear": "🔄 క్లియర్ చేయండి",
        "toast_pneumonia": "తీవ్రమైన న్యుమోనియా నమూనా లోడ్ చేయబడింది!",
        "toast_normal": "సాధారణ ఆరోగ్య నమూనా లోడ్ చేయబడింది!",
        "toast_tb": "క్షయవ్యాధి నమూనా లోడ్ చేయబడింది!",
        
        # Uploads
        "upload_section_title": "📤 రిమోట్ విశ్లేషణ కోసం మెడికల్ డేటాను అప్‌లోడ్ చేయండి",
        "col_xray_title": "📸 1. ఛాతీ ఎక్స్-రే (Chest X-ray)",
        "upload_xray_prompt": "ఎక్స్-రే ఫోటోను అప్‌లోడ్ చేయండి (PNG / JPEG)",
        "active_xray_caption": "ప్రస్తుత ఛాతీ ఎక్స్-రే",
        "col_lab_title": "📋 2. పాథాలజీ ల్యాబ్ స్లిప్ (PDF)",
        "upload_lab_prompt": "రక్త పరీక్ష / CBC నివేదిక PDF అప్‌లోడ్ చేయండి",
        "objective_title": "🎯 ఆధారిత ప్రత్యక్ష విశ్లేషణ:",
        "objective_desc": "ల్యాబ్ నివేదిక పారామితులు (WBC, CRP, ESR) మీ అధికారిక PDF నుండి నేరుగా సేకరించబడతాయి. ఎటువంటి అంచనాలు లేవు.",
        
        # Run Button
        "btn_run_triage": "🔍 హెల్త్ ట్రయాజ్ నిర్వహించండి & డాక్టర్‌ను హెచ్చరించండి",
        "warning_no_input": "దయచేసి ఎక్స్-రే, రక్త నివేదిక PDF అప్‌లోడ్ చేయండి లేదా డెమో బటన్లలో ఒకదాన్ని ఎంచుకోండి.",
        "spinner_analyzing": "ఎక్స్-రే (ResNet-50) మరియు రక్త నివేదికను (RAG) విశ్లేషిస్తోంది...",
        
        # Triage Results
        "assessment_title": "📊 తక్షణ ట్రయాజ్ ఆరోగ్య అంచనా",
        "case_label": "కేస్",
        
        # Critical Alert
        "critical_alert_badge": "🔴 అత్యవసర హెచ్చరిక: డాక్టర్‌కు వెంటనే సమాచారం పంపబడింది",
        "critical_alert_desc": "నిర్ధారించబడిన రోగనిర్ధారణ {etiology} ని సూచిస్తుంది. బంత్వాల్ ఆసుపత్రి డ్యూటీ డాక్టర్ డాక్టర్ రమేష్ రావు గారికి అత్యవసర సమాచారం చేరింది.",
        "emergency_protocol_title": "🚑 అత్యవసర ముందస్తు జాగ్రత్తలు:",
        "emergency_proto_1": "గాలి వెలుతురు ఉన్న గదిలో నిటారుగా కూర్చోండి; పడుకోవద్దు.",
        "emergency_proto_2": "ఎక్కువ శ్రమ పడవద్దు; నెమ్మదిగా లోతైన శ్వాస తీసుకోండి.",
        "emergency_proto_3": "ఫోన్ దగ్గర ఉంచుకోండి — డాక్టర్ వెంటనే కాల్ చేస్తారు.",
        "emergency_proto_4": "అత్యవసర అంబులెన్స్: డయల్ చేయండి 108",
        "contacts_title": "📞 తక్షణ అత్యవసర సహాయ కేంద్రాలు:",
        "contact_hotline": "టెలి-ఐసియు హెల్ప్‌లైన్: +91 8255 234108",
        "contact_phc": "బంత్వాల్ అత్యవసర విభాగం: 08255-232120",
        "contact_doc": "కేటాయించిన డాక్టర్: డాక్టర్ రమేష్ రావు (KMC-58291)",
        
        # Moderate & Low Risk
        "moderate_risk_title": "🟡 మధ్యస్థ ప్రమాదం: తేలికపాటి ఇన్ఫెక్షన్ లక్షణాలు",
        "moderate_risk_desc": "24 గంటల్లోపు సమీప ప్రాథమిక ఆరోగ్య కేంద్రానికి (PHC) వెళ్లండి. మీ నివేదిక డాక్టర్ పరిశీలనకు పంపబడింది.",
        "low_risk_title": "🟢 తక్కువ ప్రమాదం: సాధారణ శ్వాసకోశ పరిస్థితి",
        "low_risk_desc": "ఎక్స్-రే మరియు రక్త పరీక్షల ఫలితాలు సాధారణ పరిధిలో ఉన్నాయి. తగినంత నీరు తాగుతూ విశ్రాంతి తీసుకోండి.",
        
        # Findings Cards
        "vision_card_title": "🫁 ResNet-50 ఎక్స్-రే విశ్లేషణ",
        "vision_no_img": "ఎక్స్-రే ఏదీ అప్‌లోడ్ చేయలేదు.",
        "biomarker_card_title": "🧪 రక్త పరీక్ష నివేదిక సారాంశం",
        "biomarker_no_slip": "ల్యాబ్ స్లిప్ ఏదీ అప్‌లోడ్ చేయలేదు.",
        "pred_label": "అంచనా:",
        
        # Voice Section
        "voice_section_title": "🎙️ మీ మాతృభాషలో వైద్య సలహాను వినండి (ధ్వని సలహా)",
        "choose_audio_lang": "ఆడియో భాష:",
        "btn_play_audio": "🔊 ఆడియో వినండి (Play Audio)",
        "spinner_voice": "ఆడియో రూపొందించబడుతోంది...",
        
        # Interactive Lab Assistant
        "lab_assist_title": "💬 ఇంటరాక్టివ్ ల్యాబ్ అసిస్టెంట్ (Lab Assistant)",
        "lab_assist_desc": "మీ రక్త పరీక్ష ఫలితాల గురించి ప్రశ్నలు అడగండి.",
        
        # Tab 2: Past Results
        "past_results_title": "📬 మీ ధృవీకరించబడిన ఫలితాలు & డాక్టర్ ప్రిస్క్రిప్షన్",
        "no_cases_yet": "ఇంకా ఎటువంటి రికార్డులు లేవు. మొదటి ట్యాబ్‌లో కొత్త పరీక్షను ప్రారంభించండి!",
        "status_signed": "✅ డాక్టర్ సంతకం చేశారు",
        "status_pending": "⏳ డాక్టర్ సమీక్ష పెండింగ్‌లో ఉంది",
        "label_triage_diag": "ట్రయాజ్ రోగనిర్ధారణ:",
        "label_triage_level": "ప్రమాద స్థాయి:",
        "label_scan_finding": "స్కాన్ ఫలితం:",
        "label_biomarkers_eval": "విశ్లేషించిన బయోమార్కర్లు:",
        "label_recommendation": "సిఫార్సు:",
        "clinician_review_card": "🩺 అధికారిక వైద్యుల సమీక్ష",
        "rev_doctor": "వైద్యుడు:",
        "rev_reg": "రిజిస్ట్రేషన్ నంబర్:",
        "rev_signed": "సంతకం చేసిన సమయం:",
        "rev_prescription": "మందుల ప్రిస్క్రిప్షన్ & సూచనలు:",
        "pending_audit_title": "⏳ డాక్టర్ ధృవీకరణ పెండింగ్‌లో ఉంది",
        "pending_audit_desc": "మీ నివేదిక టెలి-ఐసియు వైద్యులకు చేరింది. పరిశీలించిన తర్వాత ప్రిస్క్రిప్షన్ ఇక్కడ కనిపిస్తుంది.",
        
        # Footer & DPDP Policies
        "footer_assistive_title": "సహాయక సాంకేతిక నోటీసు & క్లినికల్ విధానం",
        "footer_dpdp_title": "గోప్యతా విధానం & డేటా రక్షణ (DPDP చట్టం 2023)",
        "footer_dpdp_cloud": "• క్లౌడ్ నిల్వ లేదు: భారతదేశపు డిజిటల్ పర్సనల్ డేటా ప్రొటెక్షన్ (DPDP) చట్టం 2023 మరియు HIPAA భద్రతా నిబంధనల ప్రకారం, ఎక్స్-రేలు మరియు ల్యాబ్ నివేదికలు తాత్కాలిక మెమరీలో మాత్రమే ప్రాసెస్ చేయబడతాయి.",
        "footer_dpdp_phi": "• రోగి సమాచార భద్రత: రోగి గుర్తింపు వివరాలు భద్రపరచబడతాయి; ఎటువంటి బయోమెట్రిక్ చిత్రాలు పబ్లిక్ నెట్‌వర్క్‌లలో ప్రసారం చేయబడవు.",
        "footer_dpdp_chroma": "• స్థానిక ChromaDB నిల్వ: క్లినికల్ మార్గదర్శకాలు బయటికి లీక్ కాకుండా స్థానికంగా నిర్వహించబడతాయి.",
        "footer_caption": "ℹ️ నోటీసు మరియు గోప్యతా కార్డులను దాచడానికి 'సరే' క్లిక్ చేయండి.",
        "footer_btn_hide": "👁️ విధానాలను దాచండి",
        "footer_btn_show": "💡 విధాన కార్డులను చూపించండి",
        "footer_ack_tag": "🛡️ చట్టబద్ధమైన క్లినికల్ & DPDP గోప్యతా విధానాలు గుర్తించబడ్డాయి (AIIMS/ICMR/HIPAA నిబంధనల ప్రకారం)",
        "footer_expander_title": "📜 పూర్తి గోప్యతా విధానం మరియు చట్టబద్ధమైన నియంత్రణ పత్రాలను చదవండి (AIIMS, ICMR, NMC, DPDP చట్టం 2023)",
        "footer_copyright": "© 2026 మల్టీమోడಲ್ CDSS ట్రయాజ్ ప్లాట్‌ఫారమ్ | పాయింట్-ఆఫ్-కేర్ ఎడిషన్",
        "footer_statutory_standards": "చట్టబద్ధమైన ప్రమాణాలు: AIIMS క్లినికల్ AI • ICMR నైతికత 2023 • NMC చట్టం 2019 • DPDP చట్టం 2023 • HIPAA • CDSCO SaMD క్లాస్ B",
        
        # RAG Window
        "rag_lab_assistant": "ప్రయోగశాల ఫలితాల సహాయకుడు (Lab Assistant)",
        "rag_lab_subtitle": "మీ ప్రయోగశాల పరీక్ష ఫలితాల స్పష్టమైన, విశ్వసనీయ వివరణలు.",
        "rag_patient_guidance": "రోగి ఆరోగ్య మార్గదర్శకత్వం",
        "rag_quick_inquiries": "💡 శీఘ్ర క్లినికల్ ప్రశ్నలు:",
        "rag_btn_hb": "🩸 హిమోగ్లోబిన్ స్థాయి & రక్తహీనత ప్రమాదం",
        "rag_btn_wbc": "🦠 తెల్ల రక్త కణాలు (WBC) & ఇన్ఫెక్షన్ స్థితి",
        "rag_btn_glu": "🍬 బ్లడ్ గ్లూకోజ్ / షుగర్ అంచనా",
        "rag_btn_abn": "⚠️ అసాధారణ పారామితులను గుర్తించండి",
        "rag_btn_sum": "📋 రోగనిర్ధారణ ఫలితాల సారాంశం",
        "rag_btn_crit": "🚨 అత్యవసర మరియు తీవ్రమైన విలువల పరిశీలన",
        "rag_dropdown_label": "లేదా నిర్దిష్ట పరీక్షను ఎంచుకోండి:",
        "rag_dropdown_default": "-- నిర్దిష్ట పరీక్షను ఎంచుకోండి --",
        "rag_input_label": "మీ ల్యాబ్ ఫలితాల గురించి ప్రశ్న అడగండి:",
        "rag_input_placeholder": "ఉదా. అధిక WBC దేనిని సూచిస్తుంది? లేదా CRP పెరిగిందా?",
        "rag_btn_search": "🔍 శోధించండి (Search)",
        "rag_card_insight": "క్లినికల్ రిపోర్ట్ అంతర్దృష్టి",
        "rag_card_verified": "✓ ధృవీకరించబడిన సాక్ష్యం",
        "rag_card_inquiry": "అడిగిన ప్రశ్న:",
        "rag_card_footer_rec": "🔒 రోగి అధికారిక మెడికల్ రికార్డుల ఆధారంగా ధృవీకరించబడింది",
        "rag_card_footer_priv": "స్థానిక ప్రైవేట్ ప్రాసెసింగ్ (Zero Cloud Leakage)",
        "rag_btn_dismiss": "✕ మూసివేయండి (Dismiss)",
        "rag_q_hb": "హిమోగ్లోబిన్ స్థాయి ఎంత మరియు అది తక్కువగా ఉందా?",
        "rag_q_wbc": "WBC సంఖ్య ఎంత? అది అసాధారణంగా లేదా ఎక్కువగా ఉందా?",
        "rag_q_glu": "గ్లూకోజ్ స్థాయి ఎంత? అది సాధారణమేనా?",
        "rag_q_abn": "నివేదికలో కనిపించిన అన్ని అసాధారణ ల్యాబ్ పరీక్షలను జాబితా చేయండి?",
        "rag_q_sum": "ల్యాబ్ నివేదిక యొక్క ముఖ్య రోగనిర్ధారణ సారాంశాన్ని తెలపండి",
        "rag_q_crit": "ఈ నివేదికలోని అత్యవసర లేదా తీవ్రమైన విలువలు ఏమిటి?",
        
        # Biomarkers
        "biomarkers": {
            "wbc": "తెల్ల రక్త కణాలు (WBC Count)",
            "crp": "సి-రియాక్టివ్ ప్రొటీన్ (CRP)",
            "esr": "ఇ.ఎస్.ఆర్ (ESR)",
            "neutrophils": "న్యూట్రోఫిల్స్ (Neutrophils)",
            "lymphocytes": "లింఫోసైట్లు (Lymphocytes)",
            "spo2": "ఆక్సిజన్ స్థాయి (SpO2)",
            "hemoglobin": "హిమోగ్లోబిన్ (Hemoglobin)",
            "platelets": "ప్లేట్‌లెట్స్ (Platelets)"
        },
        "statuses": {
            "NORMAL": "సాధారణం (Normal)",
            "HIGH": "ఎక్కువ (High)",
            "ELEVATED": "పెరిగింది (Elevated)",
            "LOW": "తక్కువ (Low)",
            "CRITICAL": "ప్రమాదకరం (Critical)"
        }
    }
}


def get_ui_text(lang: str = "en") -> Dict[str, Any]:
    """Returns the translation dictionary for the given language, falling back to English."""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS[lang]
