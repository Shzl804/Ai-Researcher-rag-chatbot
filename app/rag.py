from pathlib import Path

from app.chunker import chunk_documents
from app.embeddings import create_embeddings
from app.pdf_loader import load_pdf
from app.text_cleaner import clean_data
from app.vector_store import VectorStore
from app.generator import AnswerGenerator

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
        self.answer_generator = AnswerGenerator()

    def index_pdf(self, pdf_path: str) -> dict:
        pages = load_pdf(pdf_path)

        cleaned_pages = []

        for page in pages:
            cleaned_pages.append(
                {
                    "text": clean_data(page["text"]),
                    "metadata": page["metadata"],
                }
            )

        chunks = chunk_documents(cleaned_pages)
        embedded_chunks = create_embeddings(chunks)
        self.vector_store.add_chunks(embedded_chunks)

        return {
            "source": Path(pdf_path).name,
            "pages": len(pages),
            "chunks": len(chunks),
        }
    def search(self, question: str, number_of_results: int= 4) -> list[dict]:
        return self.vector_store.search(
            question=question,
            number_of_results=number_of_results
        )
    def answer_question(
            self, 
            question: str,
            number_of_results: int = 4,
    ) -> dict:
        retrieved_chunks = self.search(
            question=question,
            number_of_results=number_of_results
        )
        if not retrieved_chunks:
            return {
                "answer": "I could not find the answer in the uploaded documents,",
                "sources": [],
            }
        answer = self.answer_generator.generate_answer(
            question=question,
            retrieved_chunks=retrieved_chunks,
        )

        sources = []
        seen_sources = set()

        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]

            source_key = (
                metadata["source"],
                metadata["page"]
            )

            if source_key not in seen_sources:
                sources.append(
                    {
                    "source": metadata["source"],
                    "page": metadata["page"]
                    }
                )
                seen_sources.add(source_key)

        return {
            "answer": answer,
            "sources": sources
        }