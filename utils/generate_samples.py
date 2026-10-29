"""
Synthetic Clinical Test Data Generator for CDSS
Generates realistic sample chest radiographs and hospital pathology report PDFs.
VTU 5th Sem Mini Project - Dept. of CSE (Data Science)
"""

import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont


def generate_synthetic_xray(is_pneumonia: bool = False, output_path: str = "sample_xray.png"):
    """Generates a realistic synthetic chest radiograph for local demonstration."""
    w, h = 512, 512
    # Base background: Dark exposure
    canvas = np.full((h, w), 25, dtype=np.uint8)
    
    # Thoracic ribcage oval contour
    cv2.ellipse(canvas, (256, 260), (190, 210), 0, 0, 360, 60, -1)
    
    # Left and right lung cavities (radiolucent = darker)
    # Right lung (anatomical right = viewer's left)
    cv2.ellipse(canvas, (180, 240), (65, 140), -5, 0, 360, 15, -1)
    # Left lung (anatomical left = viewer's right)
    cv2.ellipse(canvas, (330, 240), (60, 135), 5, 0, 360, 15, -1)
    
    # Heart silhouette (cardiac shadow in lower medial left cavity)
    cv2.ellipse(canvas, (280, 320), (55, 75), 25, 0, 360, 120, -1)
    
    # Spine and mediastinum (central vertical high attenuation)
    cv2.rectangle(canvas, (244, 50), (268, 480), 95, -1)
    
    # Diaphragm domes
    cv2.ellipse(canvas, (170, 390), (80, 45), 0, 0, 180, 110, -1)
    cv2.ellipse(canvas, (335, 400), (75, 40), 0, 0, 180, 105, -1)
    
    # Simulated Ribs (horizontal curvilinear white bands)
    for y in range(120, 380, 45):
        cv2.ellipse(canvas, (256, y), (170, 30), 0, 20, 160, 80, 12)
        
    # If Pneumonia: Add focal alveolar opacity / consolidation in the right mid-to-lower zone
    if is_pneumonia:
        # Patchy consolidation cloud
        opacity = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(opacity, (190, 280), 55, 145, -1)
        cv2.circle(opacity, (165, 310), 40, 130, -1)
        cv2.ellipse(opacity, (200, 250), (35, 50), -15, 0, 360, 110, -1)
        
        # Heavy Gaussian blur to simulate diffuse alveolar infiltrates
        opacity = cv2.GaussianBlur(opacity, (45, 45), 20)
        canvas = cv2.add(canvas, opacity)
        
    # Add subtle medical scan noise and smoothing
    noise = np.random.normal(0, 4, (h, w)).astype(np.int16)
    noisy_canvas = np.clip(canvas.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    smoothed = cv2.GaussianBlur(noisy_canvas, (3, 3), 0.8)
    
    # Add orientation marker "R"
    cv2.putText(smoothed, "R", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 180, 2)
    cv2.putText(smoothed, "AP CHEST", (350, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 120, 1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, smoothed)
    return output_path


def create_sample_pdf_report(patient_name: str, pid: str, is_abnormal: bool, output_path: str):
    """
    Creates a clean, realistic hospital laboratory pathology slip.
    Uses basic PDF stream generation to ensure zero external dependency failure.
    """
    if is_abnormal == "tb" or is_abnormal == "tuberculosis":
        wbc = "9,400"
        neutrophils = "52.0"
        lymphocytes = "41.5"
        crp = "18.5"
        esr = "68"
        platelets = "2.9"
        hb = "11.2"
        remarks = "Markedly elevated ESR with positive Sputum AFB smear. Correlate with chest radiography for apical/cavitary lesions. Immediate notification to NTEP / DOTS."
    elif is_abnormal:
        wbc = "15,400"
        neutrophils = "84.5"
        lymphocytes = "11.2"
        crp = "42.8"
        esr = "38"
        platelets = "2.8"
        hb = "13.2"
        remarks = "Marked polymorphonuclear leukocytosis with significant CRP elevation. Correlate with chest radiography for acute consolidation."
    else:
        wbc = "6,800"
        neutrophils = "58.0"
        lymphocytes = "34.0"
        crp = "3.2"
        esr = "12"
        platelets = "3.1"
        hb = "14.5"
        remarks = "All hematological indices within normal biological reference intervals. No acute inflammatory spikes."

    # Generate standard PDF content stream
    content = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >> endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj
6 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
4 0 obj << /Length 1200 >> stream
BT
/F1 16 Tf
50 740 Td (KIT MULTISPECIALTY HOSPITAL & DIAGNOSTICS) Tj
/F2 10 Tf
0 -18 Td (Point-of-Care Clinical Pathology Slip | Accredited Laboratory Services) Tj
0 -12 Td (Mangalore, Karnataka - 575001) Tj
0 -25 Td (========================================================================) Tj
/F1 11 Tf
0 -20 Td (PATIENT DETAILS) Tj
/F2 10 Tf
0 -15 Td (Patient Name: {patient_name}        Patient ID: {pid}) Tj
0 -15 Td (Age/Gender: 46 Y / Male              Collection Date: 18-Oct-2026) Tj
0 -15 Td (Referred By: Dr. A. K. Rao (MD Med)   Specimen: Whole Blood / Serum) Tj
0 -20 Td (------------------------------------------------------------------------------------------------------------------------) Tj
/F1 11 Tf
0 -18 Td (INVESTIGATION                      RESULT           REFERENCE RANGE        UNIT) Tj
/F2 10 Tf
0 -15 Td (------------------------------------------------------------------------------------------------------------------------) Tj
0 -16 Td (Total Leukocyte Count (TLC/WBC)    {wbc}           4,000 - 11,000         cells/uL) Tj
0 -16 Td (Neutrophils (Polymorphs)           {neutrophils}%           40.0 - 75.0            %) Tj
0 -16 Td (Lymphocytes                        {lymphocytes}%           20.0 - 45.0            %) Tj
0 -16 Td (C-Reactive Protein (Quantitative)  {crp}             0.0 - 6.0              mg/L) Tj
0 -16 Td (Erythrocyte Sedimentation Rate(ESR) {esr}               0 - 20                 mm/hr) Tj
0 -16 Td (Platelet Count                     {platelets}              1.5 - 4.5              lakhs/uL) Tj
0 -16 Td (Hemoglobin (Hb)                    {hb}             12.0 - 17.5            g/dL) Tj
0 -25 Td (========================================================================) Tj
/F1 11 Tf
0 -18 Td (PATHOLOGIST CLINICAL REMARKS) Tj
/F2 10 Tf
0 -15 Td ({remarks}) Tj
0 -40 Td (Report Verified By: Dr. S. Shenoy, Consultant Pathologist, KMC / KIT) Tj
0 -15 Td (Electronic report generated for Multimodal CDSS Decision Augmentation.) Tj
ET
endstream
endobj
xref
0 7
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000305 00000 n 
0000000219 00000 n 
0000000262 00000 n 
trailer << /Size 7 /Root 1 0 R >>
startxref
1600
%%EOF
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(content.encode("latin1"))
    return output_path


if __name__ == "__main__":
    generate_synthetic_xray(is_pneumonia=True, output_path="data/sample_xrays/patient_001_pneumonia.png")
    generate_synthetic_xray(is_pneumonia=False, output_path="data/sample_xrays/patient_002_normal.png")
    create_sample_pdf_report("Ramesh Bhat", "PID-9021", is_abnormal=True, output_path="data/sample_reports/patient_001_bacterial_pneumonia.pdf")
    create_sample_pdf_report("Sunita Patil", "PID-9022", is_abnormal=False, output_path="data/sample_reports/patient_002_normal.pdf")
    print("Sample datasets generated successfully!")
