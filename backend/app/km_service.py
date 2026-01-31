import os
from sqlalchemy.orm import Session
from .models import Document
from .core.config import settings
from .ocr import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
from .vectorstore import index_document_chunks
from .tagging import autotag

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150

def ensure_storage():
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)

def save_file(file_obj, filename: str) -> str:
    ensure_storage()
    path = os.path.join(settings.STORAGE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(file_obj)
    return path

def extract_text(path: str, mime_type: str) -> str:
    if mime_type == 'application/pdf' or path.lower().endswith('.pdf'):
        return extract_text_from_pdf(path)
    if mime_type in ('application/vnd.openxmlformats-officedocument.wordprocessingml.document',) or path.lower().endswith('.docx'):
        return extract_text_from_docx(path)
    if mime_type.startswith('image/'):
        return extract_text_from_image(path)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ''

def chunk_text(text: str):
    text = text.replace('','')
    tokens = text.split()
    chunks = []
    i = 0
    step = CHUNK_SIZE - CHUNK_OVERLAP
    while i < len(tokens):
        chunk = tokens[i:i+CHUNK_SIZE]
        chunks.append(' '.join(chunk))
        i += step
    return chunks

def create_document_from_upload(db: Session, title: str, tags: str, path: str, mime_type: str, user_id: int | None = None) -> Document:
    doc = Document(title=title, tags=tags or '', file_path=path, mime_type=mime_type, uploaded_by_id=user_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    text = extract_text(path, mime_type)
    auto = autotag(text)
    if auto and auto not in (tags or ''):
        doc.tags = ', '.join([t for t in [tags, auto] if t])
        db.commit()
        db.refresh(doc)

    chunks = chunk_text(text)
    index_document_chunks(db, doc, chunks)
    return doc

def list_documents(db: Session):
    return db.query(Document).order_by(Document.created_at.desc()).all()
