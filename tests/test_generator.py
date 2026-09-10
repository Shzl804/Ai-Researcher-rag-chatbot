SYSTEM_PROMPT = """You are a document assistant for a technical document Q&A system.

Rules:
- Answer using ONLY the information in the provided context. Never use outside knowledge.
- If the answer is not present in the context, respond exactly with:
  "I could not find the answer in the indexed documents."
- Never invent facts, page numbers, or sources that are not in the context.
- When you use information from a source, reference it using its [Source N] label.
- Keep answers concise and directly address the question — do not pad with unrelated context.
- If the context only partially answers the question, answer what you can and state what is missing.
"""

from langchain_core.messages import SystemMessage, HumanMessage

def generate_answer(self, question: str, retrieved_chunks: list[dict]):
    context = "\n\n".join(
        f"[Source {i}]\nDocument: {c['metadata']['source']}\n"
        f"Page: {c['metadata']['page']}\nText: {c['text']}"
        for i, c in enumerate(retrieved_chunks, start=1)
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{question}"),
    ]

    response = self.model.invoke(messages)
    return response.content