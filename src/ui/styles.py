"""
Module 1: UI Stylesheet & Design System
Lead: Student 1 (System Architect)
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #0A0E17 !important;
    color: #F1F5F9 !important;
}

.med-card {
    background: rgba(22, 30, 46, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}

.triage-badge-green { background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #10B981; padding: 4px 12px; border-radius: 99px; font-weight: 700; }
.triage-badge-amber { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #F59E0B; padding: 4px 12px; border-radius: 99px; font-weight: 700; }
.triage-badge-red { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid #EF4444; padding: 4px 12px; border-radius: 99px; font-weight: 700; }
</style>
"""