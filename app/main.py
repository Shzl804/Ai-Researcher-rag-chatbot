from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.rag import RAGPipeline

app = FastAPI(title="AI Researcher RAG Chatbot")

DOCUMENTS_DIR = Path("data/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

pipeline = RAGPipeline()

class QueryRequest(BaseModel):
    question: str
    number_of_results: int = 4

@app.get("/")
def home():
    return {
        "HOME": "This is AI Research ChatBot"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/documents/upload")
async def upload_documents(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF File are Supported",
        )

    file_path = DOCUMENTS_DIR / file.filename
    file_content = await file.read()
    file_path.write_bytes(file_content)

    try:
        result = pipeline.index_pdf(str(file_path))
        return result
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@app.post("/query")
def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = pipeline.answer_question(
            question=request.question,
            number_of_results=request.number_of_results
        )
        return result
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )