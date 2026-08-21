from app.embeddings import create_embeddings


def test_create_embeddings():
    chunks = [
        {
            "text": "Transformers use attention mechanisms.",
            "metadata": {
                "source": "paper.pdf",
                "page": 1,
                "chunk": 1,
            },
        },
        {
            "text": "Convolutional networks are useful for images.",
            "metadata": {
                "source": "paper.pdf",
                "page": 2,
                "chunk": 1,
            },
        },
    ]

    embedded_chunks = create_embeddings(chunks)

    assert len(embedded_chunks) == 2
    assert len(embedded_chunks[0]["embedding"]) > 0
    assert embedded_chunks[0]["text"] == chunks[0]["text"]
    assert embedded_chunks[0]["metadata"]["source"] == "paper.pdf"

    print("Embedding test passed")
    print(f"Vector dimensions: {len(embedded_chunks[0]['embedding'])}")


if __name__ == "__main__":
    test_create_embeddings()