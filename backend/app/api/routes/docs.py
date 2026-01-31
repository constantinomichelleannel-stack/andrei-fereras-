from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...schemas import DocumentOut
from ..deps import get_db, get_current_user
from ...km_service import list_documents

router = APIRouter(prefix='/docs', tags=['documents'])

@router.get('/', response_model=list[DocumentOut])
def get_docs(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_documents(db)
