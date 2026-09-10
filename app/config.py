"""
Central configuration for the RAG chatbot.
All values can be overridden via environment variables (.env).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "documents"
CHROMA_PATH = BASE_DIR / "chroma_db"

# --- Vector store ---
COLLECTION_NAME = "research_documents"

# --- Embedding model ---
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

# --- Chunking ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", ", ", " ", ""]

# --- Retrieval ---
DEFAULT_NUMBER_OF_RESULTS = int(os.getenv("DEFAULT_NUMBER_OF_RESULTS", 4))

# ChromaDB returns "distance" (lower = more similar) for cosine space.
# Chunks with a distance above this are treated as not relevant enough to use,
# so the pipeline can refuse instead of forcing the LLM to answer from noise.
SIMILARITY_DISTANCE_THRESHOLD = float(os.getenv("SIMILARITY_DISTANCE_THRESHOLD", 0.8))

# --- LLM (Groq) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0))

REQUIRED_ENV_VARS = ["GROQ_API_KEY", "GROQ_MODEL"]


def validate_env() -> None:
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Check your .env file."
        )