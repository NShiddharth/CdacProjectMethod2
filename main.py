import sys
import argparse
from typing import List, Dict

# Import components from our modular architecture
from config import LLM_API_KEY
from pdf_parser.extractor import extract_text_from_pdf
from paragrapher.segmenter import detect_paragraphs
from generator.questions import generate_questions
from generator.answers import generate_answer
from exporter.excel_writer import export_to_excel

def process_document(pdf_path: str, output_path: str) -> None:
    """
    End-to-end pipeline:
    1. Parse PDF text
    2. Segment into paragraphs
    3. Generate 10 questions per paragraph
    4. Generate an answer per question
    5. Export to Excel
    """
    
    print(f"Starting processing for: {pdf_path}")
    
    # Step 1: Extract Text
    print("Extracting text from PDF...")
    pages_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Segment Paragraphs
    print("Segmenting paragraphs...")
    paragraphs = detect_paragraphs(pages_text)
    print(f"Found {len(paragraphs)} valid paragraphs.")
    
    # Data structure to hold the final rows for Excel
    final_data: List[Dict] = []
    
    # Steps 3 & 4: Process Each Paragraph
    for para_dict in paragraphs:
        para_id = para_dict["paragraph_id"]
        para_text = para_dict["text"]
        
        print(f"\nProcessing Paragraph {para_id}...")
        
        # LLM Generation: Questions
        questions = generate_questions(para_text)
        if not questions:
            print(f"  Warning: No questions generated for Paragraph {para_id}.")
            continue
            
        print(f"  Generated {len(questions)} questions.")
        
        # LLM Generation: Answers
        for idx, question in enumerate(questions, start=1):
            print(f"    Answering question {idx}/{len(questions)}...")
            answer = generate_answer(para_text, question)
            
            # Store result
            final_data.append({
                "Paragraph_ID": para_id,
                "Question_No": idx,
                "Question": question,
                "Answer": answer
            })

    # Step 5: Export to Excel
    print(f"\nExporting {len(final_data)} total Q&A pairs to {output_path}...")
    export_to_excel(final_data, output_path)
    print("Pipeline completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="PDF to Excel Q&A Generator")
    # For user ease of use, we make them positional arguments matching standard script usage.
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_xlsx", help="Path for the output Excel file")
    
    args = parser.parse_args()
    
    try:
        process_document(args.input_pdf, args.output_xlsx)
    except Exception as e:
         print(f"Fatal error during execution: {e}", file=sys.stderr)
         sys.exit(1)

if __name__ == "__main__":
    main()
