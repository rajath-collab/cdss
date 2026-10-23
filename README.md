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

3. Install the app dependency:

   ```bash
   python -m pip install streamlit
   ```

4. Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

   Streamlit will print the local URL in the terminal (usually
   `http://localhost:8501`). Open it in a browser to use the app. Stop the
   server with `Ctrl+C`.

## Demo sign-in

- **Patient / home user:** Enter any mobile number and OTP `123456`.
- **Clinician / radiologist:** Select a medical council registration number and
  use its demo PIN:
  - `KMC-58291` — `7788`
  - `KMC-41209` — `1234`

This repository currently contains a demonstration interface. Do not use its
triage output as a diagnosis or substitute for professional medical care.
