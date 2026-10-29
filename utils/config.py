"""
Security Configuration & Environment Manager
Part of Multimodal Fused Clinical Decision Support System (CDSS)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the repository
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if it exists
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    """Centralized security and system configuration."""
    SECRET_KEY: str = os.getenv("CDSS_SECRET_KEY", "cdss_vtu_medical_secret_salt_2026_default_key")
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "12"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES: int = int(os.getenv("LOCKOUT_DURATION_MINUTES", "15"))
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    
    # Database path
    DB_PATH: str = os.getenv("DB_PATH", "data/cdss.db")
    if not os.path.isabs(DB_PATH):
        DB_PATH = str(BASE_DIR / DB_PATH)
        
    ENABLE_XSRF_PROTECTION: bool = os.getenv("ENABLE_XSRF_PROTECTION", "true").lower() in ("true", "1", "yes")


config = Config()
