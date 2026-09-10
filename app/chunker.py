from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_SEPARATORS

def chunk_documents(documents: list[dict]) -> list[dict]:
    splitters = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators=CHUNK_SEPARATORS,
    )

    chunks = []

    for document in documents:
        text_chunks = splitters.split_text(document['text'])

        for chunk_number, text in enumerate(text_chunks, start=1):
            chunks.append(
                {
                    "text": text,
                    "metadata": {
                        "source": document['metadata']['source'],
                        "page": document['metadata']['page'],
                        "chunk": chunk_number,
                    },
                }
            )
    return chunks