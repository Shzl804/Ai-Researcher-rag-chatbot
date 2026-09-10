from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL_NAME

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    def add_chunks(self, embedded_chunks: list[dict]) -> None:
        self.collection.upsert(
            ids=[
                chunk["id"]
                for chunk in embedded_chunks
            ],
            documents=[
                chunk["text"]
                for chunk in embedded_chunks
            ],
            embeddings=[
                chunk["embedding"]
                for chunk in embedded_chunks
            ],
            metadatas=[
                chunk["metadata"]
                for chunk in embedded_chunks
            ]
        )

    def search(
            self,
            question: str,
            number_of_results: int = 4,
    ) -> list[dict]:
        question_embedding =  self.embedding_model.encode(
            question,
            normalize_embeddings=True,
        ).tolist()

        results = self.collection.query(
            query_embeddings=[question_embedding],
            n_results = number_of_results,
        )

        matches = []

        for text, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            matches.append(
                {
                    "text": text,
                    "metadata": metadata,
                    "distance": distance
                }
            )

        return matches
    