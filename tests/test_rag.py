from pathlib import Path

from app.rag import RAGPipeline

def test_rag_pipeline():
    pdf_path = Path(
        "data/documents/Deep Dive into Object Tracking in Computer Vision.pdf",
    )

    pipeline = RAGPipeline()

    index_result = pipeline.index_pdf(str(pdf_path))

    print("Indexing result:")
    print(index_result)

    results = pipeline.search(
        "What is object tracking in computer vision?",
        number_of_results=3,
    )

    print("\nRetrieved results:")

    for result in results:
        print("\nText:")
        print(result["text"][:500])

        print("Metadata:")
        print(result["metadata"])

        print("Distance:")
        print(result["distance"])

    assert len(results) > 0
    assert "source" in results[0]["metadata"]
    assert "page" in results[0]["metadata"]


if __name__ == "__main__":
    test_rag_pipeline()