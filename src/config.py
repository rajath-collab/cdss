"""
Module: Global Configuration & RBAC Session State
Lead: Student 1 (System Architect)
"""
import streamlit as st

def init_session_state():
    """Initializes multi-user state variables."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = ""
    if "selected_lang" not in st.session_state:
        st.session_state["selected_lang"] = "English"
    if "current_case_id" not in st.session_state:
        st.session_state["current_case_id"] = "CASE-2026-904"

DOCTOR_DATABASE = {
    "KMC-58291": {"name": "Dr. Ramesh Rao", "pin": "7788", "dept": "Radiology"},
    "KMC-41209": {"name": "Dr. Priya Shenoy", "pin": "1234", "dept": "Pulmonology"}
}