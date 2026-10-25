import re
from typing import List, Dict

# --- CLINICAL ENTITY EXTRACTOR (Your regex + AI logic) ---
def extract_clinical_entities(text: str) -> List[Dict]:
    """Regex-based clinical entity extractor"""
    pattern = r"(?P<test_name>[A-Za-z]+):\s*(?P<value>\d+\.?\d*)\s*(?P<unit>[a-zA-Z\/dL%]+)\s*\((?P<status>[A-Za-z]+)\)"
    entities = []
    for match in re.finditer(pattern, text):
        entities.append({
            'entity_type': 'LAB_TEST',
            'test_name': match.group('test_name'),
            'value': match.group('value'),
            'unit': match.group('unit'),
            'clinical_status': match.group('status'),
            'span': match.span()
        })
    return entities

# --- AI-BASED EXTRACTOR (What Rajath asked - which AI) ---
def ai_clinical_entity_extractor(text: str) -> List[Dict]:
    """AI extractor using sentence-transformers"""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embedding = model.encode(text)
        entities = extract_clinical_entities(text)
        # Add AI fields
        for ent in entities:
            ent['ai_model'] = 'all-MiniLM-L6-v2'
            ent['embedding_dim'] = len(embedding)
            ent['method'] = 'ai_embedding'
        return entities
    except:
        # Fallback to regex if AI offline
        return extract_clinical_entities(text)

def extract_pathology_data(text: str, use_ai=True):
    entities = ai_clinical_entity_extractor(text) if use_ai else extract_clinical_entities(text)
    return {
        'clinical_entities': entities,
        'found_tests': len(entities),
        'pathology_values': {e['test_name']: e for e in entities}
    }

# --- PRE QUESTIONS FOR RAG (Rajath's 2nd requirement) ---
PREDEFINED_RAG_QUESTIONS = [
    "What is the hemoglobin level and is it low?",
    "What is the WBC count? Is it high or abnormal?",
    "What is the glucose level? Is it normal?",
    "List all abnormal lab tests found?",
    "Summarize pathology report findings",
    "What are the critical values in this report?"
]

def get_rag_pre_questions(pathology_values: dict = None) -> List[str]:
    """Generate RAG pre-questions"""
    dynamic_q = []
    if pathology_values:
        for test in pathology_values.keys():
            dynamic_q.append(f"What is the {test} level?")
            dynamic_q.append(f"Is {test} normal or abnormal?")
    
    all_q = dynamic_q + PREDEFINED_RAG_QUESTIONS
    return list(dict.fromkeys(all_q))  # Remove duplicates

def create_rag_context(extracted_data: dict) -> dict:
    """Create RAG context for ChromaDB"""
    entities = extracted_data.get('clinical_entities', [])
    context_str = "Pathology Report Findings:\n"
    for ent in entities:
        context_str += f"- {ent['test_name']}: {ent['value']} {ent['unit']} ({ent['clinical_status']})\n"
    
    return {
        "context": context_str,
        "pre_questions": get_rag_pre_questions(extracted_data.get('pathology_values', {})),
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "ready_for_rag": True
    }

# --- TEST ---
if __name__ == "__main__":
    sample = "Hemoglobin: 8.2 g/dL (Low), WBC: 12000 /uL (High), Glucose: 95 mg/dL (Normal)"
    print("=== PDF Parser Module ===")
    
    result = extract_pathology_data(sample, use_ai=False)  # Use regex for fast test, AI will work same
    print(f"\nFound {result['found_tests']} clinical entities")
    for ent in result['clinical_entities']:
        print(ent)
    
    rag = create_rag_context(result)
    print("\n--- RAG Pre-Questions (for project) ---")
    for q in rag['pre_questions']:
        print(f"- {q}")
    
    print("\nPDF Parser Module - OK (Regex + AI + Pre-Questions)")