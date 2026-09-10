# index_documents.py
from app.rag import RAGPipeline
from app.config import DATA_DIR

if __name__ == "__main__":
    pipeline = RAGPipeline()

    for pdf_path in DATA_DIR.glob("*.pdf"):
        result = pipeline.index_pdf(str(pdf_path))
        print(result)