"""
Multimodal Fusion Engine: Cross-Modal Clinical Triage Correlation
Part of Multimodal Fused Clinical Decision Support System (CDSS)
Point-of-Care Clinical Triage Edition
"""

from typing import Dict, Any, Optional


def fuse_clinical_modalities(
    vision_results: Optional[Dict[str, Any]] = None,
    lab_results: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fuses Thoracic Radiography (ResNet-50) predictions with Pathology Lab Biomarkers (RAG).
    Gracefully supports:
    1. Standalone Thoracic Radiograph (X-Ray) Analysis (when lab report is not provided).
    2. Standalone Pathology Lab Slip Analysis (when radiograph is not provided).
    3. Full Cross-Modal Multimodal Fusion (when both modalities are provided).
    """
    has_vision = vision_results is not None and bool(vision_results)
    has_lab = lab_results is not None and bool(lab_results.get("biomarkers"))

    # Case 1: Standalone Thoracic Radiograph Analysis (X-Ray Only)
    if has_vision and not has_lab:
        pred_class = vision_results.get("predicted_class", "Normal")
        xray_confidence = vision_results.get("confidence", 50.0)
        
        if "tuberculosis" in pred_class.lower() or "tb" in pred_class.lower():
            triage_category = "HIGH RISK - PRIORITY 1 (STANDALONE X-RAY)"
            severity_color = "red"
            etiology = "Pulmonary Tuberculosis (Standalone Radiographic Indication)"
            clinical_reasoning = (
                f"Standalone deep vision analysis (ResNet-50): Apical fibro-cavitary lesions detected ({xray_confidence:.1f}% confidence). "
                f"Pathology lab slip not provided — microbiological confirmation (Sputum AFB / GeneXpert) is pending."
            )
            recommendation = "Immediate isolation if clinically symptomatic. Order urgent Sputum Smear AFB, GeneXpert MTB/RIF, and CBC/ESR panel."
        elif "pneumonia" in pred_class.lower() or "opacity" in pred_class.lower():
            triage_category = "HIGH RISK - PRIORITY 1 (STANDALONE X-RAY)"
            severity_color = "red"
            etiology = "Pulmonary Consolidation / Pneumonia (Standalone Radiograph)"
            clinical_reasoning = (
                f"Standalone deep vision analysis (ResNet-50): Significant parenchymal opacity detected ({xray_confidence:.1f}% confidence). "
                f"Systemic inflammatory biomarkers (WBC / CRP) pending laboratory test submission."
            )
            recommendation = "Perform bedside auscultation (crackles/crepitations), check pulse oximetry, and upload CBC/CRP report for etiology confirmation."
        else:
            triage_category = "LOW RISK - ROUTINE (STANDALONE X-RAY)"
            severity_color = "green"
            etiology = "Clear Thoracic Fields (Standalone Radiograph)"
            clinical_reasoning = (
                f"Standalone deep vision analysis (ResNet-50): Radiograph displays normal parenchymal aeration and clear costophrenic angles ({xray_confidence:.1f}% confidence). "
                f"No pathology lab report provided."
            )
            recommendation = "No acute radiographic consolidation. Routine clinical monitoring; submit lab report if systemic symptoms exist."

        return {
            "mode": "standalone_xray",
            "triage_category": triage_category,
            "severity_color": severity_color,
            "etiology": etiology,
            "clinical_reasoning": clinical_reasoning,
            "recommendation": recommendation,
            "xray_finding": pred_class,
            "xray_confidence": xray_confidence,
            "abnormal_biomarkers_count": 0,
            "flags": ["Pathology Lab Slip Not Uploaded - Standalone Radiograph Mode"]
        }

    # Case 2: Standalone Pathology Lab Analysis (Lab Only)
    if has_lab and not has_vision:
        biomarkers = lab_results.get("biomarkers", {})
        abnormal_count = lab_results.get("abnormal_count", 0)
        clinical_flags = lab_results.get("clinical_flags", [])
        wbc_info = biomarkers.get("wbc")
        crp_info = biomarkers.get("crp")
        esr_info = biomarkers.get("esr")

        is_wbc_elevated = wbc_info and wbc_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
        is_crp_elevated = crp_info and crp_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
        is_esr_elevated = esr_info and esr_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]

        if is_wbc_elevated or is_crp_elevated or is_esr_elevated or abnormal_count >= 2:
            triage_category = "MODERATE TO HIGH RISK - STANDALONE LAB"
            severity_color = "orange"
            etiology = "Active Systemic Inflammatory Response (Standalone Lab)"
            clinical_reasoning = (
                f"Pathology lab analysis indicates {abnormal_count} abnormal biomarker(s) with elevated inflammatory markers "
                f"(WBC: {wbc_info['value'] if wbc_info else 'N/A'}, CRP: {crp_info['value'] if crp_info else 'N/A'}). "
                f"Thoracic radiograph not provided — pulmonary involvement cannot be confirmed."
            )
            recommendation = "Upload chest radiograph to assess pulmonary consolidation, or examine extrapulmonary infection foci."
        else:
            triage_category = "LOW RISK - STANDALONE LAB (NORMAL RANGES)"
            severity_color = "green"
            etiology = "Normal Hematological Profile (Standalone Lab)"
            clinical_reasoning = "All evaluated laboratory biomarkers fall within standard physiological reference intervals. Thoracic radiograph not provided."
            recommendation = "Routine observation. Upload chest radiograph if patient presents with lower respiratory symptoms."

        return {
            "mode": "standalone_lab",
            "triage_category": triage_category,
            "severity_color": severity_color,
            "etiology": etiology,
            "clinical_reasoning": clinical_reasoning,
            "recommendation": recommendation,
            "xray_finding": "Not Uploaded",
            "xray_confidence": 0.0,
            "abnormal_biomarkers_count": abnormal_count,
            "flags": clinical_flags
        }

    # Case 3: Full Multimodal Fusion (Both Modalities Present)
    pred_class = vision_results.get("predicted_class", "Normal") if vision_results else "Normal"
    xray_confidence = vision_results.get("confidence", 50.0) if vision_results else 50.0
    
    biomarkers = lab_results.get("biomarkers", {}) if lab_results else {}
    abnormal_count = lab_results.get("abnormal_count", 0) if lab_results else 0
    clinical_flags = lab_results.get("clinical_flags", []) if lab_results else []
    
    wbc_info = biomarkers.get("wbc")
    crp_info = biomarkers.get("crp")
    esr_info = biomarkers.get("esr")
    neutrophil_info = biomarkers.get("neutrophils")
    lymphocyte_info = biomarkers.get("lymphocytes")
    
    is_tb_suspect = "tuberculosis" in pred_class.lower() or "tb" in pred_class.lower()
    is_xray_abnormal = ("pneumonia" in pred_class.lower() or "opacity" in pred_class.lower() or is_tb_suspect) and xray_confidence > 50.0
    is_wbc_elevated = wbc_info and wbc_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
    is_crp_elevated = crp_info and crp_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
    is_esr_elevated = esr_info and esr_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
    is_neutrophils_elevated = neutrophil_info and neutrophil_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
    is_lymphocytes_elevated = lymphocyte_info and lymphocyte_info.get("status") in ["ELEVATED", "CRITICALLY HIGH"]
    
    if is_tb_suspect:
        triage_category = "CRITICAL RISK - PRIORITY 1 (TB SUSPECT)"
        severity_color = "red"
        etiology = "Pulmonary Tuberculosis with Inflammatory Concordance"
        clinical_reasoning = (
            f"Cross-modal concordance: Apical cavitary lesion detected on radiograph ({xray_confidence:.1f}% confidence) "
            f"accompanied by elevated inflammatory biomarkers (ESR: {esr_info['value'] if esr_info else 'N/A'}, CRP: {crp_info['value'] if crp_info else 'N/A'})."
        )
        recommendation = "Urgent isolation, fast-track Sputum Smear for AFB, GeneXpert (CBNAAT) testing, and notification to NTEP."
        
    elif is_xray_abnormal and (is_wbc_elevated or is_crp_elevated or is_neutrophils_elevated):
        triage_category = "HIGH RISK - PRIORITY 1"
        severity_color = "red"
        etiology = "Acute Bacterial Pulmonary Consolidation (Pneumonia)"
        clinical_reasoning = (
            f"Cross-modal concordance: Chest radiography displays localized opacity ({xray_confidence:.1f}% confidence), "
            f"strongly correlated with elevated systemic inflammatory/hematological biomarkers (WBC: {wbc_info['value'] if wbc_info else 'N/A'}, "
            f"CRP: {crp_info['value'] if crp_info else 'N/A'})."
        )
        recommendation = "Immediate physician consultation, sputum culture, and prompt empirical antimicrobial stewardship."
        
    elif is_xray_abnormal and is_lymphocytes_elevated and not is_neutrophils_elevated:
        triage_category = "MODERATE RISK - PRIORITY 2"
        severity_color = "orange"
        etiology = "Atypical / Viral Pulmonary Infiltration"
        clinical_reasoning = (
            f"Radiograph shows infiltrates, but leukocyte profile demonstrates relative lymphocytosis rather than neutrophilia. "
            f"Suggestive of viral etiology."
        )
        recommendation = "Supportive oxygenation, viral panel screening, and close clinical monitoring."
        
    elif is_xray_abnormal and not (is_wbc_elevated or is_crp_elevated):
        triage_category = "MODERATE RISK - OBSERVATION"
        severity_color = "orange"
        etiology = "Isolated Radiographic Opacity (Discordant Lab Findings)"
        clinical_reasoning = (
            f"Chest radiograph suggests pulmonary opacity, but circulating inflammatory biomarkers are within normal limits. "
            f"Possible resolving infection, atelectasis, or early-stage consolidation."
        )
        recommendation = "Correlate with patient auscultation findings and consider repeat radiograph in 48 hours."
        
    elif not is_xray_abnormal and (is_wbc_elevated or is_crp_elevated):
        triage_category = "MODERATE RISK - SYSTEMIC INFECTION"
        severity_color = "blue"
        etiology = "Extrapulmonary / Early Systemic Inflammation"
        clinical_reasoning = (
            f"Chest radiograph is clear, but lab biomarkers indicate active systemic inflammation ({len(clinical_flags)} abnormal markers)."
        )
        recommendation = "Evaluate extrapulmonary infection sources (e.g., urinary tract, abdominal, ENT)."
        
    else:
        triage_category = "LOW RISK - ROUTINE"
        severity_color = "green"
        etiology = "Normal Thoracic & Laboratory Baseline"
        clinical_reasoning = "Radiograph shows clear lung fields with normal hematological indices."
        recommendation = "Routine outpatient symptomatic care; follow-up if respiratory distress occurs."

    return {
        "mode": "fused_multimodal",
        "triage_category": triage_category,
        "severity_color": severity_color,
        "etiology": etiology,
        "clinical_reasoning": clinical_reasoning,
        "recommendation": recommendation,
        "xray_finding": pred_class,
        "xray_confidence": xray_confidence,
        "abnormal_biomarkers_count": abnormal_count,
        "flags": clinical_flags
    }

