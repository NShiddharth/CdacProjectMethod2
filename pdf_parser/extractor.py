import pdfplumber
from typing import List

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extracts text from a given PDF file page by page, preserving original line breaks.
    Returns a list of strings, where each string represents the text content of a single page.
    """
    pages_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # extract_text(layout=True) helps preserve visual lines though simple extract_text() usually preserves standard \n
                text = page.extract_text(layout=True)
                if text:
                    pages_text.append(text)
                else:
                    pages_text.append("")
        return pages_text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        raise
