from app.generator import AnswerGenerator


def test_groq_generation():
    generator = AnswerGenerator()

    chunks = [
        {
            "text": "Object tracking follows an object across video frames.",
            "metadata": {
                "source": "tracking.pdf",
                "page": 2,
                "chunk": 1,
            },
        }
    ]

    answer = generator.generate_answer(
        question="What is object tracking?",
        retrieved_chunks=chunks,
    )

    assert answer
    print(answer)


if __name__ == "__main__":
    test_groq_generation()