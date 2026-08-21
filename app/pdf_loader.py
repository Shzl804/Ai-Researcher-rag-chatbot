from pathlib import Path
from typing import List
import pymupdf

def load_pdf(pdf_path) -> List[dict]:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("only PDF files are supported")

    pages = []

    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text().strip()

            if text:
                pages.append(
                    {
                        "text": text,
                        "metadata": {
                            "source": path.name,
                            "page": page_number
                        }
                    }
                )
    if not pages:
        raise ValueError("The PDF contains no extractable text")

    return pages
