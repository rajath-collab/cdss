# CDSS

The Multimodal Fused Clinical Decision Support System (CDSS) is an assistive web
application designed to support point-of-care clinical triage in
resource-constrained healthcare environments. It is built with Streamlit.

## Requirements

- Python 3.10 or newer
- `pip`

## Run locally

1. Open a terminal in the project directory.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, activate it with:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

   Or run via the virtual environment directly:
   ```powershell
   .\.venv\Scripts\streamlit.exe run app.py
   ```

   **In VS Code:**
   - Press `Ctrl+Shift+B` (or **Terminal > Run Build Task**) to run the Streamlit task.
   - Or press `F5` (**Run and Debug**) to run with debugging.

   Open `http://127.0.0.1:8501` in your browser. Stop the server with `Ctrl+C`.

## Demo sign-in

- **Patient / home user:** Enter any mobile number and OTP `123456`.
- **Clinician / radiologist:** Select a medical council registration number and
  use its demo PIN:
  - `KMC-58291` — `7788`
  - `KMC-41209` — `1234`

This repository currently contains a demonstration interface. Do not use its
triage output as a diagnosis or substitute for professional medical care.
