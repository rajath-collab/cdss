# MedFuse-AI: Multimodal Point-of-Care Clinical Decision Support System (CDSS)

Comprehensive Point-of-Care Clinical Triage, Radiography Grad-CAM Explainability, and Remote Tele-ICU Frontend Platform. Built with Streamlit.

---

## 🌟 Frontend Features Included

- **Module 0: Authentication & Role-Based Access Control (RBAC)**
  - Dual Mode: Patient, Clinician (MD), and Frontline ASHA worker portals
  - 1-Click Viva Demo access buttons (`Dr. Ramesh (Doctor)`, `Rajesh (Patient)`, `Sunita (ASHA)`)
  - Full Sign-In and Registration forms with NMC State Medical Council validation
  - Inactivity timeout guard and session management
- **Module 1: Remote Patient & Home Care Portal**
  - Instant Presets: `Bacterial Pneumonia`, `Normal Baseline`, `Tuberculosis (TB)`
  - Dual modality ingestion: Chest Radiograph image uploader and Pathology Lab PDF slip uploader
  - Multimodal fused triage assessment cards (Low, Moderate, Critical)
  - Emergency Alert cards with 108 Hotline protocols
  - Vernacular voice synthesis advisory player with multi-language playback
  - Interactive Patient Laboratory Results Assistant (RAG)
  - Historical Cases & Verified Doctor E-Prescriptions tab
- **Module 2: Clinician / Radiologist Diagnostic Console & Audit**
  - Dynamic KPI cards: Pending Cases, Critical Red Flags, Validated Reports
  - Emergency Risk Alert notification banner for urgent patients
  - Multi-case selector dropdown with priority sorting
  - Dual-column inspection: Vision + Interactive Grad-CAM Heatmap Transparency Overlay slider
  - Pathology Biomarker structured table & Clinical Diagnostic Q&A Assistant
  - Official Clinical Prescription text editor with Cryptographic Digital E-Signature & dispatch
  - 108 Emergency Tele-Referral ambulance dispatch trigger
- **Module 5: Direct Multimodal Ingestion Sandbox & ASHA Field Mode**
  - Frontline ASHA worker simplified triage checklists and action plans
  - Multimodal and standalone diagnostic correlation indicators
- **Full Vernacular Localization Engine**
  - Complete translation dictionary supporting: **English, Kannada (ಕನ್ನಡ), Hindi (हिन्दी), Tamil (தமிழ்), Telugu (తెలుగు)**
- **Statutory Regulatory & Compliance Governance**
  - AIIMS Clinical AI Standards, ICMR Biomedical AI Guidelines 2023, NMC Act 2019 RMP Directives
  - DPDP Act 2023 & HIPAA Security Rules zero persistent cloud storage notice
  - Interactive show/hide notice toggles and comprehensive statutory policy expander

---

## 🚀 Running the Application

### 1. Launch with PowerShell
```powershell
cd D:\medfuse-ai
.\.venv\Scripts\streamlit.exe run app.py
```

Open your browser at: **[http://127.0.0.1:8501](http://127.0.0.1:8501)**

---

### 2. Run via Activated Virtual Environment
```powershell
cd D:\medfuse-ai
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

---

### 3. Run in VS Code (One-Click)
- **Run Build Task:** Press `Ctrl + Shift + B`
- **Run and Debug:** Press `F5`

---
