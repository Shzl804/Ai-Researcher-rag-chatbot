import os 

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class AnswerGenerator:
    def __init__(self):
        self.model = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL"),
            temperature=0
        )

    def generate_answer(
            self,
            question: str,
            retrieved_chunks: list[dict],
    ):
        context_parts = []

        for index, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk["metadata"]

            context_parts.append(
                f"[Source {index}]\n"
                f"Document: {metadata["source"]}\n"
                f"Page: {metadata['page']}\n"
                f"Text: {chunk['text']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You answer questions about technical documents.

Use only the context provided below.
Do not use outside knowledge.
If the answer is not present in the context, say:
"I could not find the answer in the uploaded documents."

Do not invent citations, page numbers, facts, or sources.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.model.invoke(prompt)

        return response.content