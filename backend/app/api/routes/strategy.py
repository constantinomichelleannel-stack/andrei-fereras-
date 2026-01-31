from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...schemas import StrategyRequest, StrategyResponse
from ..deps import get_db, get_current_user
from ...strategy import recommend

router = APIRouter(prefix='/strategy', tags=['strategy'])

@router.post('/recommend')
def recommend_strategy(req: StrategyRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return {'suggestions': recommend(req.objective, req.case_facts)}
