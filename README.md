# MedFuse-AI

Multimodal Point-of-Care Clinical Decision Support Platform. Built with Streamlit.

---

## 🌟 Frontend Modules

- **👤 Patient / Home User Portal (`src/ui/patient_view.py`):**
  - Instant presets: Bacterial Pneumonia, Normal Baseline, Tuberculosis (TB)
  - Thoracic radiograph uploader & pathology lab slip uploader
  - Clinical vitals sliders: Fever duration & SpO2 blood oxygen level
  - Automated multimodal triage assessment (Low, Moderate, Critical)
  - Emergency 108 action protocols & hotline referral contacts
  - Multi-language vernacular voice advisory preview
  - Interactive laboratory results assistant (RAG)
  - Historical cases & verified doctor prescriptions tracking
- **👨‍⚕️ Clinician / Radiologist Admin Console (`src/ui/admin_view.py`):**
  - Certified Medical Practitioner (RMP) session banner
  - Live KPI metrics cards (Pending Scans, Critical Red Flags, Validated Reports)
  - Emergency risk notification banner for high-priority patients
  - Case review queue with priority sorting
  - Dual-column inspection: Vision with interactive Grad-CAM heatmap transparency overlay slider
  - Structured pathology biomarker tables & diagnostic assistant
  - Official prescription text editor with cryptographic digital signing
  - 108 emergency tele-referral dispatch
- **💡 Statutory Compliance & Privacy (`app.py`):**
  - Assistive Technology Notice (AIIMS, ICMR, NMC, SaMD Class B) with toggle
  - DPDP Act 2023 & HIPAA Security safeguards

---

## 🚀 Running the Application

### 1. Launch Directly with PowerShell
```powershell
cd D:\medfuse-ai
.\.venv\Scripts\streamlit.exe run app.py
```

Open your browser at: **[http://localhost:8501](http://localhost:8501)**

---

### 2. Run via VS Code
- **Build Task Shortcut:** Press `Ctrl + Shift + B` (or menu: **Terminal > Run Build Task**).
- **Run & Debug:** Press `F5` (**Run and Debug**).

---

## 🔑 Verified Clinical Login Credentials

The application uses an SQLite database with 12-round Bcrypt password hashing and brute-force protection:

### 👨‍⚕️ Clinician / Radiologist (Doctor)
- **Identifier:** `dr.ramesh` or `KMC-58291`
- **Password:** `doctor123`
- **Department:** Pulmonology & Tele-ICU Center

### 👩‍⚕️ Radiologist Console
- **Identifier:** `dr.priya` or `KMC-41209`
- **Password:** `doctor123`
- **Department:** Thoracic Diagnostic Imaging

### 👤 Remote Patient Portal
- **Identifier:** `9845067890` or `patient.rajesh`
- **Password:** `patient123`

### 🤝 ASHA / Field Health Worker
- **Identifier:** `9741054321` or `asha.sunita`
- **Password:** `asha123`

*(You can also use the **Sign Up** tab to create a new patient, doctor, or ASHA account with full validation and confirm password check).*

---

## 🛡️ Security Implementation & Input Guardrails

- **Full Name Validation:** Alphabetic letters and spaces only. Strictly rejects numbers, digits, and special characters.
- **Indian Mobile Validation:** Exactly 10 digits starting with 6, 7, 8, or 9. Rejects arbitrary strings, invalid lengths, or foreign non-standard inputs.
- **Confirm Password Verification:** Enforces minimum 6 characters and matching confirmation passwords during registration.
- **ACID SQLite Database:** Persistent user accounts and authentication state in `src/security/medfuse_auth.db`.
- **Bcrypt Encryption:** Salting and hashing with 12 work rounds.
- **Brute-Force Rate Limiting:** Locks accounts for 15 minutes after 5 consecutive failed login attempts.
- **Audit Logging:** Immutable clinical session and security audit logging.

---

## 📁 Project Structure

```text
medfuse-ai/
├── app.py                     # Main application entry point & authentication router
├── requirements.txt           # Frontend dependencies
├── README.md                  # Project documentation & run guide
├── .streamlit/
│   └── config.toml            # Medical theme & server configuration
└── src/
    ├── config.py              # Session state & doctor database
    ├── rag/                   # RAG module
    ├── security/              # Security module
    ├── ui/                    # Complete Frontend User Interfaces
    │   ├── styles.py          # Custom CSS design system
    │   ├── patient_view.py    # Remote patient home care view
    │   └── admin_view.py      # Clinician / radiologist triage console
    └── vision/                # Vision deep learning module
```
