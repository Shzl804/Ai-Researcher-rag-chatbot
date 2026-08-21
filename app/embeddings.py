from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

def create_embeddings(chunks: list[dict]) -> list[dict]:
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk['text'] for chunk in chunks]
    vectors = model.encode(
        texts, 
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embedded_chunks = []

    for chunk, vector in zip(chunks, vectors):
        embedded_chunks.append(
            {
                "id" : (
                    f"{chunk['metadata']['source']}-"
                    f"page-{chunk['metadata']['page']}-"
                    f"chunk-{chunk['metadata']['chunk']}"
                ),
                "text": chunk['text'],
                "embedding": vector.tolist(),
                "metadata": chunk['metadata'],
            }
        )

    return embedded_chunks