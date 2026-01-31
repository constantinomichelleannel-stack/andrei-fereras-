from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...schemas import SearchRequest, SearchHit
from ..deps import get_db, get_current_user
from ...vectorstore import semantic_search

router = APIRouter(prefix='/search', tags=['search'])

@router.post('/semantic', response_model=list[SearchHit])
def search(req: SearchRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    hits = semantic_search(db, req.query, top_k=10)
    return [{'doc_id': i, 'title': t, 'score': s, 'snippet': snip} for (i,t,s,snip) in hits]
