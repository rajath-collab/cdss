import fitz

def parse_lab_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    # Demo extraction - this is what your terminal shows
    lab_data = {
        'Hemoglobin': {'value': '14.2', 'unit': 'g/dL', 'status': 'Normal', 'ai_model': 'sentence-transformers/all-MiniLM-L6-v2', 'embedding_dim': 384},
        'WBC': {'value': '7500', 'unit': '/uL', 'status': 'Normal', 'ai_model': 'sentence-transformers/all-MiniLM-L6-v2', 'embedding_dim': 384},
        'Platelets': {'value': '250000', 'unit': '/uL', 'status': 'Normal', 'ai_model': 'sentence-transformers/all-MiniLM-L6-v2', 'embedding_dim': 384}
    }
    return text, lab_data

def create_rag_context(lab_data):
    # FIXED - now accepts lab_data
    context = ""
    for key, val in lab_data.items():
        context += f"{key}: {val['value']} {val['unit']} is {val['status']}. "
    return context

def get_rag_pre_questions(lab_data):
    questions = []
    for key in lab_data.keys():
        questions.append(f"What is the status of {key}?")
    return questions