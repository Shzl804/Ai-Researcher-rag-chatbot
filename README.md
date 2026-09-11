# AI Researcher — RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about your own PDF documents — grounded strictly in their content, with page-level citations, and a clear refusal when the answer isn't present.

Built as part of an AI/ML Engineer Internship technical case study.

## Features

- Upload PDFs and have them automatically chunked, embedded, and indexed
- Ask natural-language questions and get answers generated only from retrieved context
- Every answer cites the source document and page number
- Refuses to answer (instead of hallucinating) when the documents don't cover the question
- FastAPI backend + Streamlit chat-style frontend
- Local, persistent vector storage (no external vector DB service required)

## How it works

```
PDF upload
  -> PyMuPDF page extraction
  -> regex-based text cleaning
  -> recursive chunking (chunk_size=1000, overlap=150)
  -> sentence-transformer embeddings (all-MiniLM-L6-v2)
  -> ChromaDB persistence
  -> similarity search on user query
  -> Groq LLM answers using only retrieved chunks
  -> answer + source citations returned
```

## Tech stack

| Layer | Choice |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| PDF parsing | PyMuPDF |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector store | ChromaDB (persistent, local) |
| LLM | Groq API |

## Project structure

```
ai-researcher-rag-chatbot/
├── app/
│   ├── main.py             # FastAPI app and routes
│   ├── config.py           # Central configuration (paths, model names, thresholds)
│   ├── pdf_loader.py        # PDF text extraction with page metadata
│   ├── text_cleaner.py     # Regex-based text cleaning
│   ├── chunker.py          # Splits cleaned text into overlapping chunks
│   ├── embeddings.py       # Converts chunks into vector embeddings
│   ├── vector_store.py     # ChromaDB storage and similarity search
│   ├── generator.py        # Groq LLM prompt + answer generation
│   └── rag.py               # Orchestrates the full pipeline
├── frontend/
│   └── streamlit_app.py    # Chat-style Streamlit UI
├── tests/                   # Unit tests per component
├── data/documents/          # Local PDFs (gitignored)
├── chroma_db/                # Vector database files (gitignored)
├── .env                      # Local secrets (gitignored)
├── requirements.txt
└── README.md
```

## Setup

**Requirements:** Python 3.10+, a Groq API key, internet access (for installing packages and downloading the embedding model on first run).

```bash
git clone https://github.com/Shzl804/Ai-Researcher-rag-chatbot.git
cd Ai-Researcher-rag-chatbot

python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

## Running the app

Start the backend:
```bash
uvicorn app.main:app --reload
```
API docs available at `http://127.0.0.1:8000/docs`

In a second terminal, start the frontend:
```bash
streamlit run frontend/streamlit_app.py
```

Open the Streamlit URL it prints, upload a PDF from the sidebar, then ask a question in the chat box.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/documents/upload` | Upload a PDF — saves it, then chunks, embeds, and indexes it |
| POST | `/documents/index` | Index a PDF already present on disk by path |
| POST | `/documents/index-folder` | Index every PDF currently in `data/documents/` |
| POST | `/query` | Ask a question; returns `{ "answer": ..., "sources": [...] }` |

## Design decisions

- **Chunk size 1000 / overlap 150** — large enough to preserve context within a chunk, with overlap so an idea split across a chunk boundary isn't lost.
- **`all-MiniLM-L6-v2` for embeddings** — small, fast, runs locally on CPU with no external API call or cost, sufficient quality for a document set of this size.
- **ChromaDB over FAISS/Pinecone** — persistent by default with a simple API, and doesn't require external infrastructure or an account, appropriate for a local/small-scale project.
- **`k=4` retrieved chunks by default** — balances enough context for the LLM against diluting the prompt with irrelevant matches; adjustable per query.
- **Similarity distance threshold** — chunks below the relevance cutoff are excluded before generation, so the model can correctly say "I don't know" instead of being handed weak matches and guessing.
- **Groq for generation** — fast inference at low cost, with `temperature=0` to keep answers deterministic and grounded rather than creative.

## Known limitations

- Basic retrieval will not reliably combine facts that require synthesizing two unrelated documents — it retrieves by similarity to the original question, not by multi-hop reasoning.
- Scaling from a handful of documents to thousands would require incremental indexing (avoiding full re-embedding) and likely a re-ranking step to keep retrieval precision high.
- Currently supports PDF input only.

## Roadmap

- [ ] Full upload-to-answer integration testing
- [ ] Improved duplicate-document handling and input validation
- [ ] Demo screenshots / screen recording
- [ ] Plain-text document support

## License

No license selected yet.