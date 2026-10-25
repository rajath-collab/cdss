import fitz
import re

def clinical_entity_extractor(text: str):
    """Clinical Entity Extractor - REAL CDSS logic"""
    entities = []
    
    # Pattern: Test Name : Value Unit (Status)
    # Example: Hemoglobin: 8.2 g/dL (Low)
    pattern = r"(?P<test>[A-Za-z\s]+?)\s*[:\-]\s*(?P<value>[\d.,]+)\s*(?P<unit>[a-zA-Z/%µL\d\-]+)?\s*(?:\((?P<status>High|Low|Normal|Abnormal)\))?"
    
    for match in re.finditer(pattern, text, re.IGNORECASE):
        entity = {
            "entity_type": "LAB_TEST",
            "test_name": match.group("test").strip(),
            "value": match.group("value").strip(),
            "unit": match.group("unit") or "N/A",
            "clinical_status": match.group("status") or "Unknown",
            "span": match.span()
        }
        entities.append(entity)
    
    return entities

def extract_pathology_data(text: str) -> dict:
    """Extract basic pathology info + Clinical Entities"""
    
    # Get clinical entities
    clinical_entities = clinical_entity_extractor(text)
    
    # Convert to simple dict for dashboard
    pathology_values = {e["test_name"].lower(): e["value"] for e in clinical_entities}
    
    return {
        "raw_text": text,
        "char_count": len(text),
        "word_count": len(text.split()),
        "clinical_entities": clinical_entities,  # <-- This is what Rajath wants!
        "pathology_values": pathology_values,
        "status": "parsed",
        "found_tests": len(clinical_entities)
    }

def extract_from_pdf(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return extract_pathology_data(text)

if __name__ == "__main__":
    print("PDF Parser Module - OK")
    sample = "Hemoglobin: 8.2 g/dL (Low), WBC: 12000 /µL (High), Glucose: 95 mg/dL (Normal)"
    result = extract_pathology_data(sample)
    print(f"Found {result['found_tests']} clinical entities")
    for ent in result['clinical_entities']:
        print(ent)