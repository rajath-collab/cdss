from pdf_parser import parse_lab_pdf, create_rag_context, get_rag_pre_questions
from vector_store import store_lab_report
from voice_engine import speak_lab_summary
import logging

logging.basicConfig(level=logging.INFO)

def main():
    pdf_path = "sample_cbc.pdf"
    logging.info(f"Processing: {pdf_path}")
    
    print("[STEP 1] Parsing PDF...")
    text, lab_data = parse_lab_pdf(pdf_path)
    print(f"[EXTRACTED] Entities: {list(lab_data.keys())}")
    print(f"[EXTRACTED] Data: {lab_data}")

    print("\n[STEP 2] Storing in Vector DB...")
    rag_context = create_rag_context(lab_data)
    store_lab_report(pdf_path, text, rag_context)
    print("[VECTOR] Stored successfully!")

    print("\n[STEP 3] Generating RAG Questions...")
    questions = get_rag_pre_questions(lab_data)
    print(f"[RAG] Pre-Questions: {questions}")

    print("\n[STEP 4] Voice Summary...")
    speak_lab_summary(lab_data)

    print("\n[SUCCESS] CDSS Pipeline Completed! ✅")

if __name__ == "__main__":
    main()