"""
Audit Logging & Clinical Governance Module
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Compliant with DPDP Act 2023 & HIPAA Security Rules (45 CFR § 164.312).
"""

from typing import List, Dict, Any, Optional
from src.security.database import get_db, get_audit_logs


def log_security_event(username: str, event_type: str, details: str = "") -> None:
    """Logs an immutable authentication or security event."""
    try:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO auth_audit_log (username, event_type, details)
                VALUES (?, ?, ?)
            """, (username, event_type, details))
    except Exception as e:
        print(f"[AuditLogger Error] Failed to write audit event: {e}")


def log_clinical_audit(doctor_id: str, case_id: str, action: str, details: str = "") -> None:
    """Logs clinician inspection, digital e-signature, or diagnosis override."""
    log_security_event(doctor_id, f"CLINICAL_{action.upper()}", f"Case: {case_id} | {details}")


def fetch_audit_trail(limit: int = 25) -> List[Dict[str, Any]]:
    """Retrieves recent audit logs."""
    return get_audit_logs(limit)


__all__ = ["log_security_event", "log_clinical_audit", "fetch_audit_trail"]
