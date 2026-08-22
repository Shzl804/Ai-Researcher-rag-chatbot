from app.embeddings import create_embeddings
from app.vector_store import VectorStore


def test_vector_store():
    chunks = [
        {
            "text": "Transformers use attention mechanisms.",
            "metadata": {
                "source": "sample.pdf",
                "page": 1,
                "chunk": 1,
            },
        },
        {
            "text": "Convolutional networks process image features.",
            "metadata": {
                "source": "sample.pdf",
                "page": 2,
                "chunk": 1,
            },
        },
    ]

    embedded_chunks = create_embeddings(chunks)

    vector_store = VectorStore()
    vector_store.add_chunks(embedded_chunks)

    results = vector_store.search(
        "How do transformers use attention?",
        number_of_results=1,
    )

    assert len(results) == 1
    assert results[0]["metadata"]["source"] == "sample.pdf"
    assert "page" in results[0]["metadata"]

    print("ChromaDB test passed")
    print(results[0])


if __name__ == "__main__":
    test_vector_store()