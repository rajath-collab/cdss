"""
Module 1: UI Stylesheet & Design System
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Glassmorphism Medical Card */
.med-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* Main Medical Banner */
.main-header {
    background: linear-gradient(135deg, #0b192c 0%, #1e3e62 100%);
    padding: 24px;
    border-radius: 12px;
    color: #ffffff;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

/* Triage Risk Badges */
.triage-badge-green {
    background: #dcfce7;
    color: #166534;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.88rem;
    display: inline-block;
    border: 1px solid #86efac;
}

.triage-badge-amber {
    background: #fef3c7;
    color: #92400e;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.88rem;
    display: inline-block;
    border: 1px solid #fde68a;
}

.triage-badge-red {
    background: #fee2e2;
    color: #991b1b;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.88rem;
    display: inline-block;
    border: 1px solid #fca5a5;
}

/* Metric KPI Cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

.stButton>button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
"""

__all__ = ["CUSTOM_CSS"]

