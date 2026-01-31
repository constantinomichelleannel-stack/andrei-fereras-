from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ...schemas import DocumentOut
from ...km_service import save_file, create_document_from_upload

router = APIRouter(prefix='/files', tags=['files'])

@router.post('/upload', response_model=DocumentOut)
async def upload_file(title: str = Form(...), tags: str = Form(''), f: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    data = await f.read()
    path = save_file(data, f.filename)
    doc = create_document_from_upload(db, title=title or f.filename, tags=tags, path=path, mime_type=f.content_type, user_id=user.id)
    return doc
