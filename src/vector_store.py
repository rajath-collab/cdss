from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    emb = model.encode(text)
    print(f"Created embedding dim {len(emb)} using all-MiniLM-L6-v2")
    return emb.tolist()

def store_lab_report(pdf_path, text, rag_context):
    combined_text = f"{pdf_path} {text} {rag_context}"
    embedding = get_embedding(combined_text)
    print(f"[VECTOR_STORE] Stored embedding for {pdf_path}")
    return embedding