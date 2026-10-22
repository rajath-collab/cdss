"""
Module 2: Clinician / Radiologist Admin Triage Console
Lead: Student 1 (System Architect)
"""
import streamlit as st

def render_admin_portal():
    st.markdown("""
        <div class="med-card">
            <h2 style="margin: 0; color: #818CF8;">👨‍⚕️ Clinician Diagnostic Console & Audit</h2>
            <p style="color: #94A3B8; margin: 4px 0 0 0;">Authorized Clinical Review, Grad-CAM Saliency Inspection, & E-Signatures.</p>
        </div>
    """, unsafe_allow_html=True)

    col_q1, col_q2, col_q3 = st.columns(3)
    col_q1.metric("Pending Remote Scans", "5 Cases")
    col_q2.metric("Critical Red Flags", "2 Urgent", delta="Immediate Action")
    col_q3.metric("Validated Today", "14 Reports", delta="+3 from Bantwal")

    st.divider()

    st.markdown("### 🔍 Case Review: `PT-2026-8491` (Bantwal PHC Home Case)")
    
    col_vis, col_rag = st.columns(2)
    with col_vis:
        st.markdown("#### Radiography Vision & Grad-CAM")
        opacity = st.slider("Grad-CAM Heatmap Transparency Overlay:", 0.0, 1.0, 0.65)
        st.caption(f"ResNet-50 Layer 4 Saliency map blended at {int(opacity*100)}% opacity.")
        # When Student 2 merges Module 3, actual model outputs will slot right here

    with col_rag:
        st.markdown("#### Pathology Biomarker Extraction (RAG)")
        st.info("• WBC: 14,200/µL (Elevated)\n• CRP: 48 mg/L (High Acute Phase Indicator)\n• Platelets: 210,000/µL (Normal)")
        # When Student 3 merges Module 4, ChromaDB outputs will slot right here

    st.divider()
    st.markdown("### ✍️ Clinician Decision Override & Digital Signature")
    doctor_notes = st.text_area("Official Clinical Prescription & Guidance:", "Right basal pneumonia confirmed. Prescribed Azithromycin 500mg OD for 3 days. Follow-up after 48h.")
    
    if st.button("🔒 Cryptographically Sign & Dispatch to Patient"):
        st.success(f"Report digitally locked with key `{st.session_state.get('user_id', 'Dr. Ramesh Rao - KMC-58291')}` and sent to the patient's phone.")