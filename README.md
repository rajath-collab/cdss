# CDSS

The Multimodal Fused Clinical Decision Support System (CDSS) is an assistive web
application designed to support point-of-care clinical triage in
resource-constrained healthcare environments. It is built with Streamlit.

## Requirements

- Python 3.10 or newer
- `pip`

## Run locally

### Quick Start (Windows PowerShell)

Run directly using the virtual environment's Streamlit executable:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Open [http://127.0.0.1:8501](http://127.0.0.1:8501) in your browser.

---

### Step-by-Step Setup

1. Open a terminal in the project directory (`medfuse-ai`).
2. Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   # If you get a script execution policy error, run this line first:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt / CMD):**
   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Streamlit app:

   ```powershell
   streamlit run app.py
   ```

   Or directly without activating:
   ```powershell
   .\.venv\Scripts\streamlit.exe run app.py
   ```

   **In VS Code:**
   - Press `Ctrl+Shift+B` (or **Terminal > Run Build Task**) to run the predefined Streamlit task.
   - Or press `F5` (**Run and Debug**) to launch with debugging.

---

### Troubleshooting Common Issues

* **Error: `Port 8501 is not available`**
  This happens when a previous Streamlit or Python background instance was not cleanly stopped. Run this PowerShell command to terminate the hung process:
  ```powershell
  Stop-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess -Force
  ```
  Then restart Streamlit:
  ```powershell
  .\.venv\Scripts\streamlit.exe run app.py
  ```

* **Error: `'streamlit' is not recognized as the name of a cmdlet`**
  Your virtual environment is not active in the current terminal window. Either activate it first or use the direct path:
  ```powershell
  .\.venv\Scripts\streamlit.exe run app.py
  ```

* **Error: `Activate.ps1 cannot be loaded because running scripts is disabled`**
  Allow script execution for the current session:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\.venv\Scripts\Activate.ps1
  ```

## Demo sign-in

- **Patient / home user:** Enter any mobile number and OTP `123456`.
- **Clinician / radiologist:** Select a medical council registration number and
  use its demo PIN:
  - `KMC-58291` — `7788`
  - `KMC-41209` — `1234`

This repository currently contains a demonstration interface. Do not use its
triage output as a diagnosis or substitute for professional medical care.
