import fitz

def extract_pathology_data(text: str) -> dict:
    """Extract basic pathology info"""
    return {
        "raw_text": text,
        "char_count": len(text),
        "word_count": len(text.split()),
        "status": "parsed"
    }

def extract_from_pdf(pdf_path: str) -> dict:
    """Read PDF and then extract"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return extract_pathology_data(text)

if __name__ == "__main__":
    print("PDF Parser Module - OK")