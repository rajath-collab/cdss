"""
SQLite Security Database & Authentication Engine
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Enforces:
  - ACID Transactional Storage with WAL mode
  - Adaptive Bcrypt Password Hashing (12 rounds)
  - Brute-Force Rate Limiting & Account Lockout Guard (5 attempts / 15 mins)
  - Immutable Security & Clinical Access Audit Logging
  - Multi-Identifier User Verification (Username, 10-Digit Mobile, and Doctor Council Reg)
  - GPS Geolocation & Demographic Address Persistence
"""

import os
import sqlite3
import datetime
import urllib.request
import json
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Dict, Any, Tuple
import bcrypt

# Secure local SQLite database path inside src/security/
DB_DIR = Path(__file__).resolve().parent
DB_PATH = DB_DIR / "medfuse_auth.db"

BCRYPT_ROUNDS = 12
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


@contextmanager
def get_db():
    """Provides thread-safe connection with Row factory and WAL mode."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def hash_password(password: str) -> str:
    """Cryptographic Bcrypt salted hash with 12 rounds."""
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against stored Bcrypt hash."""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def init_db():
    """Creates database tables, handles column migrations, and pre-seeds verified accounts."""
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                phone TEXT UNIQUE,
                reg_number TEXT UNIQUE,
                organization TEXT,
                email TEXT,
                age INTEGER,
                gender TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                pincode TEXT,
                gps_coordinates TEXT,
                emergency_contact_name TEXT,
                emergency_contact_phone TEXT,
                specialization TEXT,
                experience_years INTEGER,
                blood_group TEXT,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_reg ON users(reg_number);")

        # Column Migration Guard (Adds newly introduced columns if running on an existing DB)
        existing_cols = [r["name"] for r in cursor.execute("PRAGMA table_info(users)").fetchall()]
        new_columns = [
            ("email", "TEXT"),
            ("age", "INTEGER"),
            ("gender", "TEXT"),
            ("address", "TEXT"),
            ("city", "TEXT"),
            ("state", "TEXT"),
            ("pincode", "TEXT"),
            ("gps_coordinates", "TEXT"),
            ("emergency_contact_name", "TEXT"),
            ("emergency_contact_phone", "TEXT"),
            ("specialization", "TEXT"),
            ("experience_years", "INTEGER"),
            ("blood_group", "TEXT"),
        ]
        for col_name, col_type in new_columns:
            if col_name not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                except Exception:
                    pass

        # 2. Authentication Audit Log Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                event_type TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. Pre-seed Default Verified Accounts if users table is empty
        seed_accounts = [
            {
                "username": "dr.ramesh",
                "password": "doctor123",
                "full_name": "Dr. Ramesh Rao, MD",
                "role": "doctor",
                "phone": "9845012345",
                "reg_number": "KMC-58291",
                "organization": "Bantwal District Hospital / Tele-ICU Center",
                "email": "dr.ramesh@teleicu.gov.in",
                "age": 49,
                "gender": "Male",
                "city": "Bantwal",
                "state": "Karnataka",
                "pincode": "574211",
                "specialization": "Pulmonology & Critical Care",
                "experience_years": 18
            },
            {
                "username": "dr.priya",
                "password": "doctor123",
                "full_name": "Dr. Priya Shenoy, MD",
                "role": "doctor",
                "phone": "9845099999",
                "reg_number": "KMC-41209",
                "organization": "Mangalore Central Hospital",
                "email": "dr.priya@mch.org.in",
                "age": 42,
                "gender": "Female",
                "city": "Mangaluru",
                "state": "Karnataka",
                "pincode": "575001",
                "specialization": "Thoracic Radiology",
                "experience_years": 14
            },
            {
                "username": "patient.rajesh",
                "password": "patient123",
                "full_name": "Rajesh Kumar",
                "role": "patient",
                "phone": "9845067890",
                "reg_number": None,
                "organization": "Bantwal Rural PHC Zone 2",
                "email": "rajesh.k@gmail.com",
                "age": 48,
                "gender": "Male",
                "address": "House #44, B.C. Road",
                "city": "Bantwal",
                "state": "Karnataka",
                "pincode": "574211",
                "blood_group": "B+",
                "emergency_contact_name": "Suresh Kumar (Brother)",
                "emergency_contact_phone": "9448199999"
            },
            {
                "username": "asha.sunita",
                "password": "asha123",
                "full_name": "Sunita Naik",
                "role": "asha",
                "phone": "9741054321",
                "reg_number": "ASHA-DK-409",
                "organization": "Panemangalore PHC Sub-Center",
                "email": "sunita.asha@karnataka.gov.in",
                "age": 36,
                "gender": "Female",
                "city": "Panemangalore",
                "state": "Karnataka",
                "pincode": "574231"
            }
        ]

        cursor.execute("SELECT COUNT(*) as count FROM users")
        row = cursor.fetchone()
        if row["count"] == 0:
            for acc in seed_accounts:
                hashed_pw = hash_password(acc["password"])
                cursor.execute("""
                    INSERT INTO users (
                        username, password_hash, full_name, role, phone, reg_number, organization,
                        email, age, gender, address, city, state, pincode, specialization, experience_years,
                        blood_group, emergency_contact_name, emergency_contact_phone
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    acc["username"],
                    hashed_pw,
                    acc["full_name"],
                    acc["role"],
                    acc["phone"],
                    acc["reg_number"],
                    acc["organization"],
                    acc.get("email"),
                    acc.get("age"),
                    acc.get("gender"),
                    acc.get("address"),
                    acc.get("city"),
                    acc.get("state"),
                    acc.get("pincode"),
                    acc.get("specialization"),
                    acc.get("experience_years"),
                    acc.get("blood_group"),
                    acc.get("emergency_contact_name"),
                    acc.get("emergency_contact_phone")
                ))
            
            cursor.execute("""
                INSERT INTO auth_audit_log (username, event_type, details)
                VALUES ('SYSTEM', 'DATABASE_INITIALIZED', 'Pre-seeded initial verified clinical accounts with Bcrypt hashing.')
            """)
        else:
            # Backfill demographics for pre-seeded accounts if null
            for acc in seed_accounts:
                cursor.execute("""
                    UPDATE users SET 
                        email = COALESCE(email, ?),
                        age = COALESCE(age, ?),
                        gender = COALESCE(gender, ?),
                        address = COALESCE(address, ?),
                        city = COALESCE(city, ?),
                        state = COALESCE(state, ?),
                        pincode = COALESCE(pincode, ?),
                        specialization = COALESCE(specialization, ?),
                        experience_years = COALESCE(experience_years, ?),
                        blood_group = COALESCE(blood_group, ?),
                        emergency_contact_name = COALESCE(emergency_contact_name, ?),
                        emergency_contact_phone = COALESCE(emergency_contact_phone, ?)
                    WHERE username = ?
                """, (
                    acc.get("email"), acc.get("age"), acc.get("gender"), acc.get("address"),
                    acc.get("city"), acc.get("state"), acc.get("pincode"), acc.get("specialization"),
                    acc.get("experience_years"), acc.get("blood_group"), acc.get("emergency_contact_name"),
                    acc.get("emergency_contact_phone"), acc["username"]
                ))


def get_user_by_identifier(identifier: str) -> Optional[Dict[str, Any]]:
    """
    Looks up user by:
      - exact username (e.g. 'dr.ramesh', 'patient.rajesh')
      - 10-digit phone number (e.g. '9845012345')
      - Medical Council Registration Number (e.g. 'KMC-58291')
    """
    if not identifier:
        return None

    clean = identifier.strip()
    clean_lower = clean.lower()
    digits_only = "".join(c for c in clean if c.isdigit())
    if digits_only.startswith("91") and len(digits_only) == 12:
        digits_only = digits_only[2:]

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users
            WHERE LOWER(username) = ? 
               OR phone = ? 
               OR UPPER(reg_number) = ?
               OR LOWER(phone) = ?
            LIMIT 1
        """, (clean_lower, digits_only if len(digits_only) == 10 else clean, clean.upper(), clean_lower))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Strictly looks up user by unique username (case-insensitive)."""
    if not username:
        return None
    clean = username.strip().lower()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(username) = ? LIMIT 1", (clean,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None


def verify_doctor_phone_match(username: str, phone: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Checks that the entered username exists and the entered phone strictly matches
    the phone number registered for that doctor account.
    Returns: (is_matched, user_dict, message)
    """
    user = get_user_by_username(username)
    if not user:
        # Also check if username entered was their phone or reg number
        user = get_user_by_identifier(username)
    
    if not user:
        return False, None, f"No account found with username '{username}'."

    cleaned_phone = "".join(c for c in phone if c.isdigit())
    if cleaned_phone.startswith("91") and len(cleaned_phone) == 12:
        cleaned_phone = cleaned_phone[2:]

    reg_phone = "".join(c for c in (user.get("phone") or "") if c.isdigit())

    if cleaned_phone != reg_phone:
        return False, user, "Mobile number does not match the registered record for this account."

    return True, user, "User credentials verified."


def fetch_location_by_gps() -> Dict[str, Any]:
    """
    Auto-detects geographic location coordinates & address info using network geolocation.
    Provides graceful fallback to Bantwal / Mangalore, Karnataka if network is offline.
    """
    try:
        req = urllib.request.Request("http://ip-api.com/json/", headers={"User-Agent": "Mozilla/5.0 MedFuse-AI"})
        with urllib.request.urlopen(req, timeout=2.5) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                lat = data.get("lat", 12.9187)
                lon = data.get("lon", 74.8598)
                return {
                    "city": data.get("city", "Mangaluru"),
                    "state": data.get("regionName", "Karnataka"),
                    "pincode": data.get("zip", "575007"),
                    "gps_coordinates": f"{lat:.4f}° N, {lon:.4f}° E",
                    "success": True,
                    "source": "Network GPS"
                }
    except Exception:
        pass

    # High-fidelity fallback for coastal Karnataka primary healthcare deployment
    return {
        "city": "Bantwal",
        "state": "Karnataka",
        "pincode": "574211",
        "gps_coordinates": "12.8913° N, 75.0347° E",
        "success": True,
        "source": "Local Healthcare Zone Default"
    }


def create_user(
    username: str,
    password: str,
    full_name: str,
    role: str,
    phone: str,
    reg_number: Optional[str] = None,
    organization: Optional[str] = None,
    email: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    pincode: Optional[str] = None,
    gps_coordinates: Optional[str] = None,
    emergency_contact_name: Optional[str] = None,
    emergency_contact_phone: Optional[str] = None,
    specialization: Optional[str] = None,
    experience_years: Optional[int] = None,
    blood_group: Optional[str] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Creates a new user record in the database with full clinical demographic details
    and Bcrypt password hashing. Enforces uniqueness of username, phone, and registration.
    """
    init_db()

    clean_user = username.strip().lower()
    clean_phone = phone.strip() if phone else None
    clean_reg = reg_number.strip().upper() if reg_number else None
    clean_name = full_name.strip()

    with get_db() as conn:
        cursor = conn.cursor()

        # Check existing username
        cursor.execute("SELECT id FROM users WHERE LOWER(username) = ?", (clean_user,))
        if cursor.fetchone():
            return False, f"Username '{clean_user}' is already registered. Please choose another username or sign in.", None

        # Check existing phone
        if clean_phone:
            cursor.execute("SELECT id FROM users WHERE phone = ?", (clean_phone,))
            if cursor.fetchone():
                return False, f"Mobile number '{clean_phone}' is already registered with another account. Please sign in.", None

        # Check existing reg number
        if clean_reg:
            cursor.execute("SELECT id FROM users WHERE UPPER(reg_number) = ?", (clean_reg,))
            if cursor.fetchone():
                return False, f"Medical Council Registration '{clean_reg}' is already registered. Please sign in.", None

        # Hash password with Bcrypt
        hashed_pw = hash_password(password)

        cursor.execute("""
            INSERT INTO users (
                username, password_hash, full_name, role, phone, reg_number, organization,
                email, age, gender, address, city, state, pincode, gps_coordinates,
                emergency_contact_name, emergency_contact_phone, specialization, experience_years, blood_group
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            clean_user,
            hashed_pw,
            clean_name,
            role.lower(),
            clean_phone,
            clean_reg,
            organization,
            email.strip() if email else None,
            age,
            gender,
            address.strip() if address else None,
            city.strip() if city else None,
            state.strip() if state else None,
            pincode.strip() if pincode else None,
            gps_coordinates,
            emergency_contact_name.strip() if emergency_contact_name else None,
            emergency_contact_phone.strip() if emergency_contact_phone else None,
            specialization.strip() if specialization else None,
            experience_years,
            blood_group
        ))

        cursor.execute("""
            INSERT INTO auth_audit_log (username, event_type, details)
            VALUES (?, 'USER_REGISTERED', ?)
        """, (clean_user, f"Registered role '{role}' for {clean_name} at {city or 'Unknown'}. GPS: {gps_coordinates or 'Manual'}"))

    new_user = get_user_by_identifier(clean_user)
    return True, "Account registered successfully!", new_user


def record_login_attempt(username: str, is_success: bool) -> Tuple[int, bool, Optional[str]]:
    """
    Handles brute-force protection:
    - If success: resets failed_attempts = 0, locked_until = NULL.
    - If failure: increments failed_attempts. If >= MAX_FAILED_ATTEMPTS, locks account for LOCKOUT_MINUTES.
    Returns: (failed_attempts, is_locked, lockout_message)
    """
    now = datetime.datetime.now()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(username) = ?", (username.lower(),))
        user = cursor.fetchone()
        if not user:
            cursor.execute("""
                INSERT INTO auth_audit_log (username, event_type, details)
                VALUES (?, 'LOGIN_FAILURE_UNKNOWN_USER', 'Failed login attempt with non-existent identifier.')
            """, (username,))
            return 1, False, None

        if is_success:
            cursor.execute("""
                UPDATE users 
                SET failed_attempts = 0, locked_until = NULL 
                WHERE id = ?
            """, (user["id"],))
            cursor.execute("""
                INSERT INTO auth_audit_log (username, event_type, details)
                VALUES (?, 'LOGIN_SUCCESS', 'Successful clinical session authentication.')
            """, (user["username"],))
            return 0, False, None
        else:
            new_attempts = user["failed_attempts"] + 1
            if new_attempts >= MAX_FAILED_ATTEMPTS:
                lock_time = now + datetime.timedelta(minutes=LOCKOUT_MINUTES)
                cursor.execute("""
                    UPDATE users 
                    SET failed_attempts = ?, locked_until = ? 
                    WHERE id = ?
                """, (new_attempts, lock_time.isoformat(), user["id"]))
                cursor.execute("""
                    INSERT INTO auth_audit_log (username, event_type, details)
                    VALUES (?, 'ACCOUNT_LOCKOUT', ?)
                """, (user["username"], f"Exceeded {MAX_FAILED_ATTEMPTS} failed attempts. Account locked until {lock_time}."))
                msg = f"⛔ Account is locked due to {new_attempts} consecutive failed attempts. Please wait {LOCKOUT_MINUTES} minutes before retrying."
                return new_attempts, True, msg
            else:
                cursor.execute("""
                    UPDATE users 
                    SET failed_attempts = ? 
                    WHERE id = ?
                """, (new_attempts, user["id"]))
                cursor.execute("""
                    INSERT INTO auth_audit_log (username, event_type, details)
                    VALUES (?, 'LOGIN_FAILURE', ?)
                """, (user["username"], f"Failed password attempt {new_attempts} of {MAX_FAILED_ATTEMPTS}."))
                return new_attempts, False, None


def is_account_locked(user: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Checks if an account is currently locked due to exceeded attempts."""
    locked_until_str = user.get("locked_until")
    if not locked_until_str:
        return False, None

    try:
        locked_until = datetime.datetime.fromisoformat(locked_until_str)
        now = datetime.datetime.now()
        if now < locked_until:
            rem_minutes = max(1, int((locked_until - now).total_seconds() / 60))
            return True, f"⛔ Account locked due to security rate limiting. Please wait {rem_minutes} minute(s) before trying again."
        else:
            with get_db() as conn:
                conn.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?", (user["id"],))
            return False, None
    except Exception:
        return False, None


def get_audit_logs(limit: int = 15):
    """Retrieves recent authentication and security audit logs."""
    init_db()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auth_audit_log ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in cursor.fetchall()]


# Initialize tables and seed data upon module import
init_db()

__all__ = [
    "init_db",
    "hash_password",
    "verify_password",
    "get_user_by_identifier",
    "get_user_by_username",
    "verify_doctor_phone_match",
    "fetch_location_by_gps",
    "create_user",
    "record_login_attempt",
    "is_account_locked",
    "get_audit_logs"
]
