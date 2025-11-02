import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str):
    with fitz.open(file_path) as pdf:
        for page in pdf:
            yield page.get_text()
