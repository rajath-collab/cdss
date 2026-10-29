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

## 🔑 Demo Sign-In Credentials

### 👤 Patient Portal
- **Mobile Number:** `9845012345` (or click 1-Click Instant Demo)
- **Demo OTP:** `123456`

### 👨‍⚕️ Clinician / Radiologist Console
- **Medical Council Reg No:** `KMC-58291` (Dr. Ramesh Rao)
- **Doctor Security PIN:** `7788` (or click 1-Click Instant Demo)

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
