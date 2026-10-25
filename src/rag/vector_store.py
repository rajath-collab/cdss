import chromadb

# In-memory client for testing, persistent later
client = chromadb.Client()
collection = client.get_or_create_collection(name="pathology_reports")

def add_report(report_id: str, text: str, metadata: dict = None):
    """Add pathology report to vector DB"""
    try:
        collection.add(
            ids=[report_id],
            documents=[text],
            metadatas=[metadata or {"source": "lab"}]
        )
        return True
    except Exception as e:
        print(f"Add Error: {e}")
        return False

def query_reports(query_text: str, n_results: int = 3):
    """Search similar reports"""
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"Query Error: {e}")
        return {"documents": []}

if __name__ == "__main__":
    print("Vector Store Module - OK")
    add_report("test_01", "Hemoglobin 12.5 g/dL Normal")
    print(query_reports("hemoglobin"))