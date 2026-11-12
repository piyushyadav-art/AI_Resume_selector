from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str | Path): The path to the PDF file.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = pymupdf.open(pdf_path)
    try:
        pages = []
        full_text_parts = []
        for page_number, page in enumerate(document, start=1):
            text = page.get_text()
            pages.append({
                "page_number": page_number,
                "text": text
            })
            full_text_parts.append(text)
    finally:
        document.close()

    return {
        "total_pages": len(pages),
        "full_text": "\n".join(full_text_parts).strip(),
        "pages": pages
    }
