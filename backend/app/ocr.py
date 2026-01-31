import os, tempfile, subprocess
import pytesseract
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document as Docx

def extract_text_from_pdf(path: str) -> str:
    try:
        text = pdf_extract_text(path) or ''
        if text.strip():
            return text
    except Exception:
        pass
    out_text = []
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, 'page')
        subprocess.run(['pdftoppm', '-r', '300', path, base, '-png'], check=True)
        for name in sorted(os.listdir(tmp)):
            if name.endswith('.png'):
                img_path = os.path.join(tmp, name)
                out_text.append(pytesseract.image_to_string(img_path))
    return '
'.join(out_text)

def extract_text_from_docx(path: str) -> str:
    doc = Docx(path)
    return '
'.join(p.text for p in doc.paragraphs)

def extract_text_from_image(path: str) -> str:
    return pytesseract.image_to_string(path)
