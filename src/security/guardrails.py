"""
Security Guardrails & Input Validation Engine
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Enforces:
  - Full Name Validation (alphabetical characters only, strictly no numbers or symbols)
  - Strict Indian 10-Digit Mobile Number Validation (6-9 prefix, no arbitrary strings)
  - Medical Council Registration Format (NMC Act 2019 / State Council verification)
  - Email Address & Postal Pincode Format
  - Password Strength & Confirm Password Matching
"""

import re
from typing import Tuple

# Recognized State Medical Council & National Medical Commission Prefixes
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
    "NMC": "National Medical Commission"
}

# Council registration pattern: e.g. KMC-58291, MMC-41209, NMC-2024-1234
COUNCIL_REGEX = re.compile(
    r"^(?P<council>[A-Z]{2,5})[-/ ](?P<seq>[0-9]{4,8}(?:-[0-9]{2,4})?)$",
    re.IGNORECASE
)

# Standard Email Regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Indian Postal Pincode Regex (6 digits, first digit 1-9)
PINCODE_REGEX = re.compile(r"^[1-9][0-9]{5}$")


def validate_full_name(name: str) -> Tuple[bool, str]:
    """
    Validates that Full Name contains strictly letters and spaces.
    Rejects numbers, digits, symbols, or single-character names.
    """
    if not name or not name.strip():
        return False, "Full Name cannot be empty. Please enter your name."
    
    clean_name = name.strip()

    # Reject if any numbers/digits are present
    if re.search(r"\d", clean_name):
        return False, "Full Name cannot contain numbers or digits. Please enter alphabetic characters only."

    # Validate allowed characters: English letters, spaces, dots, hyphens, apostrophes
    if not re.match(r"^[A-Za-z\s.'-]{2,60}$", clean_name):
        return False, "Full Name must contain only alphabetic letters and spaces (2 to 60 characters)."

    # Must contain at least two actual alphabetic letters
    letters = re.findall(r"[A-Za-z]", clean_name)
    if len(letters) < 2:
        return False, "Full Name must contain at least 2 alphabetic letters."

    return True, ""


def validate_phone_number(phone: str) -> Tuple[bool, str, str]:
    """
    Validates a 10-digit Indian mobile number.
    Accepts raw 10 digits or numbers with +91 / 0 prefix.
    Rejects letters, random lengths, and numbers starting with 0-5.
    Returns: (is_valid, error_message, cleaned_10_digit_number)
    """
    if not phone or not phone.strip():
        return False, "Mobile phone number cannot be empty.", ""

    raw = phone.strip()

    # Normalize: strip out spaces, dashes, parentheses
    cleaned = re.sub(r"[\s\-\(\)]", "", raw)

    # Strip leading +91 or 91 if followed by 10 digits
    if cleaned.startswith("+91") and len(cleaned) == 13:
        cleaned = cleaned[3:]
    elif cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = cleaned[1:]

    # Check for non-digit characters
    if not cleaned.isdigit():
        return False, "Mobile number must contain digits only. Letters and special symbols are not allowed.", ""

    # Check exact 10 digits
    if len(cleaned) != 10:
        return False, f"Mobile number must be exactly 10 digits (you entered {len(cleaned)} digits).", ""

    # Check valid Indian mobile starting prefix (6, 7, 8, 9)
    if cleaned[0] not in ["6", "7", "8", "9"]:
        return False, f"Invalid mobile prefix '{cleaned[0]}'. Valid Indian mobile numbers must start with 6, 7, 8, or 9.", ""

    # Check against repetitive dummy numbers like 0000000000 or 1111111111
    if len(set(cleaned)) == 1:
        return False, "Invalid mobile number: repetitive digits detected.", ""

    return True, "", cleaned


def validate_email(email: str) -> Tuple[bool, str]:
    """Validates standard email format."""
    if not email or not email.strip():
        return True, "" # Optional field
    clean = email.strip()
    if not EMAIL_REGEX.match(clean):
        return False, "Please enter a valid email address (e.g., name@hospital.org)."
    return True, ""


def validate_pincode(pincode: str) -> Tuple[bool, str]:
    """Validates Indian 6-digit postal pincode."""
    if not pincode or not pincode.strip():
        return True, "" # Optional
    clean = pincode.strip()
    if not PINCODE_REGEX.match(clean):
        return False, "Postal Pincode must be a valid 6-digit number."
    return True, ""


def validate_doctor_reg(reg_number: str) -> Tuple[bool, str, str]:
    """
    Validates a doctor's State Medical Council or NMC registration identifier.
    Returns: (is_valid, error_message, normalized_reg)
    """
    if not reg_number or not reg_number.strip():
        return False, "Medical Council Registration number cannot be empty for Doctor registration.", ""

    clean_reg = reg_number.strip().upper()
    match = COUNCIL_REGEX.match(clean_reg)
    if not match:
        return False, (
            "Invalid council registration format. Expected format: Council-Sequence "
            "(e.g., KMC-58291, MMC-41209, or NMC-2024-1234)."
        ), ""

    council = match.group("council").upper()
    if council not in RECOGNIZED_COUNCILS:
        allowed = ", ".join(RECOGNIZED_COUNCILS.keys())
        return False, f"Unrecognized Medical Council code '{council}'. Supported codes: {allowed}.", ""

    return True, "", clean_reg


def validate_password(password: str, confirm_password: str = None) -> Tuple[bool, str]:
    """
    Validates password length, security, and checks confirm_password matching.
    """
    if not password:
        return False, "Password cannot be empty."

    if len(password) < 6:
        return False, f"Password must be at least 6 characters long (currently {len(password)} characters)."

    if confirm_password is not None:
        if password != confirm_password:
            return False, "Passwords do not match. Please re-enter identical passwords in both fields."

    return True, ""


__all__ = [
    "validate_full_name",
    "validate_phone_number",
    "validate_email",
    "validate_pincode",
    "validate_doctor_reg",
    "validate_password",
    "RECOGNIZED_COUNCILS"
]
