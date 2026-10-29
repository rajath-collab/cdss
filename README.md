# Multimodal Fused Clinical Decision Support System (CDSS)
**MedFuse-AI | Dept. of CSE (Data Science), KIT, Mangalore | VTU 5th Sem Mini Project**

An explainable, multimodal point-of-care artificial intelligence platform engineered to augment clinical triage in resource-constrained healthcare environments (Primary Health Centres, Tele-ICU networks, and rural ASHA frontline workers).

---

## 🚀 Quick Start (Running the Application)

### 1. Launch Directly in Windows PowerShell

Run the Streamlit application using the project virtual environment:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Open your browser at: **[http://127.0.0.1:8501](http://127.0.0.1:8501)**

---

### 2. Run via VS Code (One-Click)

- **Default Build Task:** Press `Ctrl + Shift + B` (or menu: **Terminal > Run Build Task**) to start the Streamlit UI task.
- **Run & Debug:** Press `F5` to start debugging with `launch.json`.

---

### 3. Step-by-Step Setup from a Fresh Terminal

If setting up the environment from scratch:

```powershell
# 1. Open PowerShell in project directory (d:\medfuse-ai)
# If script execution is disabled, enable it for this session:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Verify / install dependencies (if needed)
pip install -r requirements.txt

# 4. Start the application
streamlit run app.py
```

---

#