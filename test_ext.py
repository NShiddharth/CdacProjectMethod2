from pdf_parser.extractor import extract_text_from_pdf
from paragrapher.segmenter import detect_paragraphs
import sys

pdf_path = "13363.pdf"
pages_text = extract_text_from_pdf(pdf_path)
print(f"Original single extract: {len(detect_paragraphs(pages_text))} paragraphs")

import pdfplumber
def test_layout(pdf_path):
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True)
            if text: pages_text.append(text)
    return pages_text

pt_layout = test_layout(pdf_path)
paras = detect_paragraphs(pt_layout)
print(f"Layout=True extract: {len(paras)} paragraphs")
