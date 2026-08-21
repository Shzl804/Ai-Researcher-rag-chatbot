from pathlib import Path

from app.pdf_loader import load_pdf

documents_dir = Path("data/documents")

for path_pdf in documents_dir.glob("*.pdf"):
    try: 
        pages = load_pdf(str(path_pdf))

        print(f"\n {path_pdf.name}")
        print(f"Extracted pages: {len(pages)}")
        print(f"First Page Preview: {pages[0]['text'][:200]}")
        print(f"MetaData: {pages[0]['metadata']}")
    except Exception as error:
        print(f"{path_pdf.name}: Error - {error}")