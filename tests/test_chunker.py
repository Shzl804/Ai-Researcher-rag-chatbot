from app.chunker import chunk_documents


def test_chunk_documents():
    documents = [
        {
            "text": (
                "This is a long sample document. " * 100
            ),
            "metadata": {
                "source": "sample.pdf",
                "page": 1,
            },
        }
    ]

    chunks = chunk_documents(documents)

    assert len(chunks) > 1

    for chunk in chunks:
        assert chunk["text"]
        assert chunk["metadata"]["source"] == "sample.pdf"
        assert chunk["metadata"]["page"] == 1
        assert "chunk" in chunk["metadata"]

    print(f"Created {len(chunks)} chunks")
    print("Chunking test passed")


if __name__ == "__main__":
    test_chunk_documents()