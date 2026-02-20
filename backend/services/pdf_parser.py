import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() or ""

    return full_text