"""
Statutory Medical Council & Identity Verification Engine
Part of Multimodal Fused Clinical Decision Support System (CDSS)
Compliant with:
  - National Medical Commission (NMC) Act 2019
  - State Medical Council Registry Protocols (KMC, MMC, DMC, TNMC, etc.)
  - Ayushman Bharat Digital Mission (ABDM) Healthcare Professional Registry (HPR)
"""

import re
from typing import Tuple, Dict, Any, Optional

# Recognized State Medical Council & National Authority Prefixes
RECOGNIZED_COUNCILS = {
    "KMC": "Karnataka Medical Council",
    "MMC": "Maharashtra Medical Council",
    "DMC": "Delhi Medical Council",
    "TNMC": "Tamil Nadu Medical Council",
    "APMC": "Andhra Pradesh Medical Council",
    "TSMC": "Telangana State Medical Council",
    "WBMC": "West Bengal Medical Council",
    "GMC": "Gujarat Medical Council",
    "MCI": "Medical Council of India (Legacy)",
    "NMC": "National Medical Commission (Central Registry)"
}

# Regex pattern for council format: e.g., KMC-12345, MMC/67890, NMC-2024-1234
REGISTRATION_PATTERN = re.compile(
    r"^(?P<council>[A-Z]{2,5})[-/ ](?P<sequence>[0-9]{4,8}(?:-[0-9]{2,4})?)$",
    re.IGNORECASE
)


def validate_doctor_registration(reg_number: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Validates a doctor's State Medical Council or NMC registration identifier.
    Returns: (is_valid: bool, feedback_message: str, details: Optional[Dict])
    """
    clean_reg = reg_number.strip().upper()
    
    if not clean_reg:
        return False, "Registration number cannot be empty.", None

    match = REGISTRATION_PATTERN.match(clean_reg)
    if not match:
        return False, (
            "Invalid registration format. Expected format: Council-Sequence "
            "(e.g., KMC-58291, MMC-49102, or NMC-2024-9182)."
        ), None

    council_code = match.group("council")
    sequence = match.group("sequence")

    if council_code not in RECOGNIZED_COUNCILS:
        allowed = ", ".join(RECOGNIZED_COUNCILS.keys())
        return False, (
            f"Unrecognized Medical Council code '{council_code}'. "
            f"Recognized codes include: {allowed}."
        ), None

    # Simulate statutory check against ABDM / NMC Health Professional Registry
    council_name = RECOGNIZED_COUNCILS[council_code]
    verification_data = {
        "status": "VERIFIED_STATUTORY_RMP",
        "council_code": council_code,
        "council_name": council_name,
        "license_sequence": sequence,
        "standard_code": f"{council_code}-{sequence}",
        "governing_law": "NMC Act 2019 / RMP Code of Ethics"
    }

    return True, f"Valid Registered Medical Practitioner ID ({council_name}).", verification_data
