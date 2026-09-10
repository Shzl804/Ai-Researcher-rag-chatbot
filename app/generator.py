import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, GROQ_MODEL, LLM_TEMPERATURE

load_dotenv()

class AnswerGenerator:
    def __init__(self):
        self.model = None
        if GROQ_API_KEY:
            self.model = ChatGroq(
                api_key=GROQ_API_KEY,
                model=GROQ_MODEL,
                temperature=LLM_TEMPERATURE,
            )

    def generate_answer(
            self,
            question: str,
            retrieved_chunks: list[dict],
    ):
        if self.model is None:
            raise ValueError(
                "GROQ_API_KEY is not configured. Add it to your .env file before asking questions."
            )

        context_parts = []

        for index, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk["metadata"]

            context_parts.append(
                f"[Source {index}]\n"
                f"Document: {metadata['source']}\n"
                f"Page: {metadata['page']}\n"
                f"Text: {chunk['text']}"
            )

        context = "\n\n".join(context_parts)

        PROMPT_TEMPLATE = """You are a document assistant for a technical document Q&A system.

Rules:
- Answer using ONLY the information in the context below. Never use outside knowledge.
- If the answer is not present in the context, respond exactly with:
  "I could not find the answer in the indexed documents."
- Never invent facts, page numbers, or sources that are not in the context.
- When you use information from a source, reference it using its [Source N] label.
- Keep answers concise and directly address the question.
- If the context only partially answers the question, answer what you can and state what is missing.

Context:
{context}

Question:
{question}

Answer:
"""

        prompt = PROMPT_TEMPLATE.format(context=context, question=question)
        response = self.model.invoke(prompt)

        return response.content