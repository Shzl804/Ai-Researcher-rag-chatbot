# AI Researcher RAG Chatbot

An educational retrieval-augmented generation (RAG) project for asking
questions about technical PDF documents. The project is being built
incrementally to demonstrate the main steps of a document-based AI system:
PDF extraction, text cleaning, chunking, embeddings, vector search, and
grounded answer generation.

## Project Status

The project is currently in MVP development. The document processing,
embedding, vector storage, RAG pipeline, Groq generation, FastAPI backend, and
Streamlit interface are implemented. Final end-to-end verification and
hardening are still pending.

Implemented:

- Page-by-page PDF text extraction with source and page metadata
- Basic text cleaning with regular expressions
- Recursive text chunking with metadata preservation
- Sentence-transformer embeddings using `all-MiniLM-L6-v2`
- Persistent ChromaDB storage and similarity search
- Groq-powered grounded answer generation
- FastAPI health and query endpoints
- Tests for the document-processing and vector-store components

Still to verify or improve:

- Full upload-to-answer integration testing
- Improved duplicate document handling and error validation

The application is not yet a complete chat interface.

## Problem

Technical information is often spread across research papers, notes, and
documentation. This project aims to help a student or researcher upload those
documents and ask questions while seeing the source document and page used for
the answer.

Example question:

```text
What is the main contribution of this paper?
```

The intended answer flow is:

```text
PDF
	-> extract page text
	-> clean text
	-> create chunks
	-> create embeddings
	-> store in ChromaDB
	-> retrieve relevant chunks
	-> ask Groq using retrieved context
	-> return answer and citations
```

## Technology Stack

- Python
- FastAPI backend API
- Streamlit frontend
- PyMuPDF for PDF text extraction
- Python regular expressions for basic text cleaning
- LangChain text splitters for chunking
- Sentence Transformers for embeddings
- `all-MiniLM-L6-v2` for a small local embedding model
- ChromaDB for persistent local vector storage
- Groq API for answer generation
- Git and GitHub for version control

## Project Structure

```text
ai-researcher-rag-chatbot/
├── app/
│   ├── chunker.py          # Split extracted text into chunks
│   ├── config.py           # Application configuration placeholder
│   ├── embeddings.py       # Create sentence-transformer embeddings
│   ├── main.py             # FastAPI application and routes
│   ├── pdf_loader.py       # Extract PDF text with page metadata
│   ├── rag.py              # Indexing, retrieval, and answer orchestration
│   └── text_cleaner.py     # Remove unwanted text patterns
├── data/
│   └── documents/          # Local PDFs; ignored by Git
├── chroma_db/              # Local vector database; ignored by Git
├── tests/
│   ├── test_chunker.py
│   ├── test_embeddings.py
│   ├── test_pdf_loader.py
│   └── test_text_cleaner.py
├── frontend/
│   └── streamlit_app.py    # Streamlit frontend
├── .env                    # Local secrets; ignored by Git
├── .gitignore
├── plan.text               # Full MVP development plan
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Git
- Internet access for installing packages and downloading the embedding model
- A Groq API key for answer generation

The current embedding tests run locally on CPU. A GPU is not required.

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/YOUR_USERNAME/ai-researcher-rag-chatbot.git
cd ai-researcher-rag-chatbot
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Debian-based Linux systems, do not install these project packages into the
system Python. Use the project `.venv` as shown above.

## Environment Variables

Create a local `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=your_available_groq_model
```

Never commit `.env` or a real API key. The `.gitignore` file excludes `.env`.

## Add Documents

Place local PDF files in:

```text
data/documents/
```

These files are intentionally ignored by Git. Do not upload private documents,
large files, or documents you are not allowed to redistribute to GitHub.

## Run Tests

Run commands from the repository root with the virtual environment activated:

```bash
python -m tests.test_pdf_loader
python -m tests.test_text_cleaner
python -m tests.test_chunker
python -m tests.test_embeddings
python -m tests.test_vector_store
python -m tests.test_rag
python -m tests.test_generator
```

The embedding test may take longer the first time because
`all-MiniLM-L6-v2` must be downloaded and loaded. It produces vectors with
384 dimensions.

## Current Learning Objectives

This project is also a learning exercise. The important concepts are:

1. Extract text while preserving document location metadata.
2. Clean text without destroying useful technical information.
3. Split long documents into retrieval-friendly chunks.
4. Convert each chunk into a numerical embedding.
5. Store and search embeddings using a vector database.
6. Generate answers only from retrieved context.
7. Show source citations instead of relying on unsupported model claims.

## Security and Repository Rules

Do not commit:

- `.env` files or API keys
- `.venv/`
- `chroma_db/`
- Private or copyrighted PDFs in `data/documents/`
- Python cache files

Before committing, check the files Git will include:

```bash
git status
git diff --cached
```

## Run the FastAPI Backend

Start the API from the repository root:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

### `GET /`

Returns a basic application message.

### `GET /health`

Checks that the API is running.

```bash
curl http://127.0.0.1:8000/health
```

### `POST /query`

Retrieves relevant chunks and asks Groq to generate a grounded answer.

```bash
curl -X POST \\
	-H "Content-Type: application/json" \\
	-d '{"question":"What is machine learning?","number_of_results":4}' \\
	http://127.0.0.1:8000/query
```

The response contains an answer and source metadata with document names and
page numbers.

## Run the Streamlit Frontend

Start FastAPI first in one terminal:

```bash
uvicorn app.main:app --reload
```

Start Streamlit from the repository root in another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

The interface lets you check the backend, ask a question, and view the
generated answer with source page citations. The frontend uses
`http://127.0.0.1:8000` by default. Set `API_URL` in `.env` to use a
different backend URL.

## RAG Pipeline

The current backend follows this flow:

```text
PDF upload
	-> PyMuPDF page extraction
	-> regex text cleaning
	-> recursive chunking
	-> all-MiniLM-L6-v2 embeddings
	-> ChromaDB persistence
	-> similarity retrieval
	-> Groq prompt with retrieved context
	-> answer and source metadata
```

The application creates citations from ChromaDB metadata instead of asking the
LLM to invent page numbers.

## Roadmap

The MVP will be completed in this order:

1. Verify the complete upload-to-answer workflow.
2. Improve validation and duplicate document handling.
3. Add screenshots and a short demo.
4. Add further features only after the MVP is stable.

More detailed steps are in [plan.text](plan.text).

## License

No license has been selected yet. Add an appropriate license before treating
this repository as a public reusable project.
