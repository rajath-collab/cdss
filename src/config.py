"""
Module: Global Configuration & RBAC Session State
MedFuse-AI - Multimodal Clinical Decision Support System
"""
import streamlit as st
from utils.config import config

def init_session_state():
    """Initializes multi-user state variables."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = ""
    if "ui_lang" not in st.session_state:
        st.session_state["ui_lang"] = "en"
    if "selected_lang" not in st.session_state:
        st.session_state["selected_lang"] = "English"
    if "current_case_id" not in st.session_state:
        st.session_state["current_case_id"] = "PT-2026-8491"

DOCTOR_DATABASE = {
    "KMC-58291": {"name": "Dr. Ramesh Rao, MD", "pin": "7788", "dept": "Radiology", "hospital": "Bantwal District Hospital"},
    "KMC-41209": {"name": "Dr. Priya Shenoy, MD", "pin": "1234", "dept": "Pulmonology", "hospital": "Mangalore Central Hospital"}
}

__all__ = ["init_session_state", "DOCTOR_DATABASE", "config"]
