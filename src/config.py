"""
Module: Global Configuration, State & Clinical Data Manager
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
"""
import streamlit as st
import time

DOCTOR_DATABASE = {
    "KMC-58291": {
        "name": "Dr. Ramesh Rao, MD (Pulmonology)",
        "pin": "7788",
        "dept": "Pulmonology & Tele-ICU",
        "hospital": "Bantwal District Hospital / Tele-ICU Center"
    },
    "KMC-41209": {
        "name": "Dr. Priya Shenoy, MD (Radiology)",
        "pin": "1234",
        "dept": "Thoracic Diagnostic Imaging",
        "hospital": "Mangalore Central Hospital"
    }
}

DEFAULT_PATIENT_CASES = {
    "PT-2026-8491": {
        "case_id": "PT-2026-8491",
        "patient_username": "+91 9845012345",
        "patient_name": "Rajesh Kumar",
        "patient_age": 48,
        "patient_gender": "Male",
        "location": "Bantwal Rural PHC Zone 2",
        "emergency_contact": "+91 94481 99999",
        "timestamp": "2026-10-29 18:30:15",
        "xray_preset": "patient_001_pneumonia",
        "xray_finding": "Pneumonia / Consolidation",
        "xray_confidence": 92.4,
        "lab_biomarkers": {
            "wbc": {"name": "White Blood Cell Count", "value": "14,200", "unit": "/µL", "status": "ELEVATED", "normal_range": "4,500 - 11,000 /µL"},
            "crp": {"name": "C-Reactive Protein", "value": "48.0", "unit": "mg/L", "status": "CRITICALLY HIGH", "normal_range": "< 5.0 mg/L"},
            "esr": {"name": "Erythrocyte Sed. Rate", "value": "38", "unit": "mm/hr", "status": "ELEVATED", "normal_range": "0 - 15 mm/hr"},
            "neutrophils": {"name": "Neutrophil %", "value": "81", "unit": "%", "status": "ELEVATED", "normal_range": "40 - 70 %"}
        },
        "triage_summary": {
            "triage_category": "CRITICAL RISK - PRIORITY 1",
            "severity_color": "red",
            "etiology": "Acute Bacterial Pulmonary Consolidation with Elevated Inflammatory Biomarkers",
            "clinical_reasoning": "Cross-modal concordance: Chest radiograph displays localized opacity (92.4% confidence) coupled with critically elevated inflammatory markers (WBC: 14,200/µL, CRP: 48 mg/L).",
            "recommendation": "URGENT INTERVENTION: Emergency tele-consultation triggered. Initiate empirical IV antibiotic therapy and close clinical monitoring at Bantwal PHC."
        },
        "is_critical": True,
        "alert_status": "🚨 URGENT ACTION NEEDED (Acute Consolidation & Elevated CRP)",
        "doctor_review": {
            "status": "pending_review",
            "doctor_name": None,
            "doctor_reg": None,
            "reviewed_at": None,
            "prescription": "Right basal bacterial pneumonia confirmed with acute hypoxia. Prescribed: Tab Azithromycin 500mg OD x 3 days, Tab Paracetamol 650mg SOS. Administer nasal cannula O2 @ 2L/min at Bantwal PHC. Immediate tele-follow up in 24 hours.",
            "doctor_notes": None
        }
    },
    "PT-2026-8492": {
        "case_id": "PT-2026-8492",
        "patient_username": "+91 9741054321",
        "patient_name": "Sita Devi",
        "patient_age": 34,
        "patient_gender": "Female",
        "location": "Panemangalore Sub-Center",
        "emergency_contact": "+91 97410 00111",
        "timestamp": "2026-10-29 19:15:00",
        "xray_preset": "patient_002_normal",
        "xray_finding": "Normal Baseline",
        "xray_confidence": 98.1,
        "lab_biomarkers": {
            "wbc": {"name": "White Blood Cell Count", "value": "6,800", "unit": "/µL", "status": "NORMAL", "normal_range": "4,500 - 11,000 /µL"},
            "crp": {"name": "C-Reactive Protein", "value": "2.4", "unit": "mg/L", "status": "NORMAL", "normal_range": "< 5.0 mg/L"}
        },
        "triage_summary": {
            "triage_category": "LOW RISK - ROUTINE BASELINE",
            "severity_color": "green",
            "etiology": "Clear Lung Parenchyma with Normal Inflammatory Profile",
            "clinical_reasoning": "Radiograph displays bilateral clear lung fields with normal physiological hematological markers.",
            "recommendation": "Maintain adequate oral hydration. Routine outpatient follow-up."
        },
        "is_critical": False,
        "alert_status": "✅ Routine Baseline",
        "doctor_review": {
            "status": "reviewed",
            "doctor_name": "Dr. Ramesh Rao, MD (Pulmonology)",
            "doctor_reg": "KMC-58291",
            "reviewed_at": "2026-10-29 20:00:10",
            "prescription": "Normal baseline confirmed. Reassure patient; maintain oral hydration and return if respiratory distress develops.",
            "doctor_notes": "All parameters normal."
        }
    }
}

LANGUAGES = {
    "en": {"name": "English", "native": "English", "flag": "🌐"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ (Kannada)", "flag": "🇮🇳"},
    "hi": {"name": "Hindi", "native": "हिन्दी (Hindi)", "flag": "🇮🇳"},
    "ta": {"name": "Tamil", "native": "தமிழ் (Tamil)", "flag": "🇮🇳"},
    "te": {"name": "Telugu", "native": "తెలుగు (Telugu)", "flag": "🇮🇳"},
    "ml": {"name": "Malayalam", "native": "മലയാളം (Malayalam)", "flag": "🇮🇳"}
}

def init_session_state():
    """Initializes session state variables for authentication, triage, and multi-user simulation."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = ""
    if "ui_lang" not in st.session_state:
        st.session_state["ui_lang"] = "en"
    if "hide_assistive_notice" not in st.session_state:
        st.session_state["hide_assistive_notice"] = False
    if "last_activity" not in st.session_state:
        st.session_state["last_activity"] = time.time()
    if "patient_cases" not in st.session_state:
        st.session_state["patient_cases"] = dict(DEFAULT_PATIENT_CASES)

__all__ = ["init_session_state", "DOCTOR_DATABASE", "DEFAULT_PATIENT_CASES", "LANGUAGES"]
