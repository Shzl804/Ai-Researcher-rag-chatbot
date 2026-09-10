from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.config import DATA_DIR, validate_env
from app.rag import RAGPipeline

app = FastAPI(title="AI Researcher RAG Chatbot")
pipeline = RAGPipeline()

DATA_DIR.mkdir(parents=True, exist_ok=True)


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


@app.post("/documents/query")
@app.post("/query")
def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        validate_env()
        result = pipeline.answer_question(
            question=request.question,
            number_of_results=request.number_of_results,
        )
        return result
    except EnvironmentError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/documents/index")
@app.post("/index")
def index_document(pdf_path: str):
    try:
        return pipeline.index_pdf(pdf_path)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/documents/upload")
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    save_path = DATA_DIR / file.filename

    try:
        with open(save_path, "wb") as file_handle:
            file_handle.write(await file.read())
        return pipeline.index_pdf(str(save_path))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/documents/index-folder")
@app.post("/index-folder")
def index_folder():
    return pipeline.index_directory(DATA_DIR)