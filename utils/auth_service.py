"""
Authentication & Role-Based Access Control (RBAC) Module
Part of Multimodal Fused Clinical Decision Support System (CDSS)
Hardened with:
  - Adaptive Bcrypt password hashing (12 rounds)
  - Seamless legacy SHA-256 hash auto-migration
  - Brute-force protection & account lockout rate limiting
  - Transactional SQLite backing store
"""

import os
import hashlib
from typing import Dict, Any, Optional, Tuple
import bcrypt

from utils.config import config
from utils.db_manager import (
    db_get_user,
    db_get_all_users,
    db_create_user,
    db_update_user_password,
    db_record_login_attempt,
    db_get_recent_failed_attempts,
    db_clear_login_attempts,
    db_log_audit
)


def hash_password(password: str) -> str:
    """Cryptographic Bcrypt hash with adaptive work factor."""
    salt = bcrypt.gensalt(rounds=config.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def _legacy_sha256_hash(password: str) -> str:
    """Legacy SHA-256 hash with internal salt (for backward migration only)."""
    salt = "cdss_vtu_medical_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def verify_password(plain_password: str, stored_hash: str) -> Tuple[bool, bool]:
    """
    Verifies plain password against stored hash.
    Returns: (is_valid: bool, needs_rehash_migration: bool)
    """
    if not stored_hash:
        return False, False
        
    # Check if hash is Bcrypt ($2a$, $2b$, or $2y$)
    if stored_hash.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            is_valid = bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8"))
            return is_valid, False
        except Exception:
            return False, False

    # Check against legacy SHA-256
    legacy_hash = _legacy_sha256_hash(plain_password)
    if legacy_hash == stored_hash:
        # Password matches legacy hash; signal that it should be upgraded to bcrypt
        return True, True

    return False, False


def _bootstrap_default_accounts() -> None:
    """Bootstraps default demo accounts with Bcrypt if not present."""
    default_users = [
        {
            "username": "dr.ramesh",
            "password": "doctor123",
            "role": "doctor",
            "full_name": "Dr. Ramesh Rao, MD (Pulmonology)",
            "meta": {
                "reg_number": "KMC-58291",
                "hospital": "Bantwal District Hospital / Tele-ICU Center",
                "phone": "+91 98450 12345",
                "email": "dr.ramesh@karnataka.gov.in"
            }
        },
        {
            "username": "patient.rajesh",
            "password": "patient123",
            "role": "patient",
            "full_name": "Rajesh Kumar",
            "meta": {
                "patient_id": "PT-2026-8491",
                "age": 48,
                "gender": "Male",
                "phone": "+91 94481 67890",
                "address": "Bantwal Rural PHC Zone 2",
                "emergency_contact": "+91 94481 99999"
            }
        },
        {
            "username": "asha.sunita",
            "password": "asha123",
            "role": "asha",
            "full_name": "Sunita Naik (ASHA Lead)",
            "meta": {
                "worker_id": "ASHA-DK-409",
                "sub_center": "Panemangalore PHC Sub-Center",
                "phone": "+91 97410 54321"
            }
        }
    ]
    for u in default_users:
        if not db_get_user(u["username"]):
            db_create_user(
                username=u["username"],
                password_hash=hash_password(u["password"]),
                role=u["role"],
                full_name=u["full_name"],
                meta=u["meta"]
            )


# Initialize default accounts if database is fresh
_bootstrap_default_accounts()


def load_users() -> Dict[str, Any]:
    """Compatibility method returning all users from SQLite."""
    return db_get_all_users()


def save_users(users: Dict[str, Any]) -> None:
    """Compatibility method: writes user dictionaries to SQLite."""
    for uname, udata in users.items():
        if not db_get_user(uname):
            meta = {k: v for k, v in udata.items() if k not in ["username", "password_hash", "role", "full_name"]}
            db_create_user(
                username=uname,
                password_hash=udata.get("password_hash", ""),
                role=udata.get("role", "patient"),
                full_name=udata.get("full_name", uname),
                meta=meta
            )


def authenticate_user(username: str, password: str, client_ip: str = "127.0.0.1") -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Validates user credentials with adaptive bcrypt verification,
    brute-force rate limiting, and account lockout.
    Returns: (success: bool, user_data: Optional[Dict], message: str)
    """
    clean_user = username.strip().lower()
    if not clean_user:
        return False, None, "Please provide a valid username."

    # 1. Check for Active Account Lockout
    failed_attempts = db_get_recent_failed_attempts(clean_user, config.LOCKOUT_DURATION_MINUTES)
    if failed_attempts >= config.MAX_LOGIN_ATTEMPTS:
        db_log_audit(clean_user, "unknown", "LOGIN_BLOCKED_LOCKOUT", details=f"Attempts: {failed_attempts}")
        return False, None, f"⚠️ Account temporarily locked due to {failed_attempts} failed login attempts. Please wait {config.LOCKOUT_DURATION_MINUTES} minutes before trying again."

    # 2. Query User Record
    user = db_get_user(clean_user)
    if not user:
        db_record_login_attempt(clean_user, is_success=False, ip_address=client_ip)
        return False, None, "Username not found. Please register or check spelling."

    # 3. Cryptographic Verification & Rehash Migration
    is_valid, needs_upgrade = verify_password(password, user.get("password_hash", ""))
    
    if not is_valid:
        db_record_login_attempt(clean_user, is_success=False, ip_address=client_ip)
        attempts_now = failed_attempts + 1
        remaining = max(0, config.MAX_LOGIN_ATTEMPTS - attempts_now)
        if remaining > 0:
            return False, None, f"Invalid password. {remaining} attempt(s) remaining before temporary lockout."
        else:
            return False, None, f"⚠️ Maximum attempts exceeded. Account locked for {config.LOCKOUT_DURATION_MINUTES} minutes."

    # 4. Success Path: Clear Lockout History
    db_record_login_attempt(clean_user, is_success=True, ip_address=client_ip)
    db_clear_login_attempts(clean_user)

    # 5. Auto-Migrate Legacy SHA-256 Hash to Bcrypt
    if needs_upgrade:
        new_bcrypt_hash = hash_password(password)
        db_update_user_password(clean_user, new_bcrypt_hash)
        user["password_hash"] = new_bcrypt_hash
        db_log_audit(clean_user, user.get("role", "patient"), "PASSWORD_MIGRATED_BCRYPT")

    db_log_audit(clean_user, user.get("role", "patient"), "LOGIN_SUCCESS", details=f"Role: {user.get('role')}")
    return True, user, f"Welcome back, {user.get('full_name', username)}!"


def register_user(
    username: str,
    password: str,
    role: str,
    full_name: str,
    extra_meta: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    """
    Registers a new patient, clinician, or ASHA worker in SQLite.
    Returns: (success: bool, message: str)
    """
    clean_user = username.strip().lower()
    
    if not clean_user or not password:
        return False, "Username and password cannot be empty."
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    if db_get_user(clean_user):
        return False, f"Username '{clean_user}' already exists. Please choose another or sign in."
    
    # Hash password with Bcrypt
    secure_hash = hash_password(password)
    
    success = db_create_user(
        username=clean_user,
        password_hash=secure_hash,
        role=role,
        full_name=full_name.strip(),
        meta=extra_meta
    )
    
    if success:
        db_log_audit(clean_user, role, "USER_REGISTERED", details=f"Full Name: {full_name.strip()}")
        return True, "Account created successfully! You can now sign in."
    else:
        return False, "An error occurred while creating your account. Please try again."
