# PDF to Excel Q&A Generator

A modular Python pipeline that takes a PDF document, segments the text into clear paragraphs, and uses an LLM to automatically generate diverse Question & Answer pairs based *strictly* on each paragraph. The final output is neatly exported into an Excel file.

## Features
- **PDF Parsing**: Robust text extraction from multi-page PDFs using `pdfplumber`.
- **Paragraph Segmentation**: Rule-based text cleanup and logical paragraph grouping.
- **LLM-Powered Generation**: Generates exactly 10 diverse questions (avoiding repetitive "What" questions) per valid paragraph and accurately answers them using only the context given.
- **Excel Export**: Saves the resultant DataFrame into an easy-to-read `.xlsx` file containing: Paragraph ID, Question No, Question, and Answer.
- **Modular Architecture**: Clean separation of extraction, segmentation, generation, and output logic.

## Prerequisites
- Python 3.8+
- An LLM API key. By default, the project expects an `NVIDIA_API_KEY` or `LLM_API_KEY` (set as an environment variable or via a `.env` file) to access standard OpenAI-compatible endpoints.

## Installation

1. **Clone the repository or navigate to the project directory:**
   ```bash
   cd vacant-blazar
   ```

2. **(Optional but recommended) Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The project can be configured via a `.env` file or directly through environment variables.
Create a `.env` file in the project root with the following:

```env
NVIDIA_API_KEY=your_api_key_here
# Optionally specify an alternative model
LLM_MODEL=meta/llama-3.1-8b-instruct
```

You can view `config.py` for more default settings such as the minimum words per paragraph, generation models, and customized LLM prompts.

## Usage

You can run the full end-to-end processing pipeline using `main.py`. It requires two positional arguments: the input PDF path and the output Excel path.

```bash
python main.py <input_pdf_path> <output_xlsx_path>
```

**Example:**
```bash
python main.py sample_document.pdf output_questions.xlsx
```

The script will print progress to the standard output and, upon successful completion, your Q&A pairs will be ready in `output_questions.xlsx`.

## Project Structure
```
├── config.py             # Configuration, prompts, and environment validation
├── main.py               # Main CLI entry point handling the pipeline
├── requirements.txt      # Python dependencies
├── .env                  # Environment Variables (Create this manually)
├── pdf_parser/
│   └── extractor.py      # PDF text extraction module
├── paragrapher/
│   └── segmenter.py      # Cleans and splits text into structured paragraphs
├── generator/
│   ├── questions.py      # Calls LLM to produce structured Question JSON
│   └── answers.py        # Calls LLM to produce Answers using the Question+Context
└── exporter/
    └── excel_writer.py   # Generates output Excel format using Pandas/OpenPyXL
```

## License
MIT License
