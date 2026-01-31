from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...schemas import PredictRequest, PredictResponse
from ..deps import get_db, get_current_user
from ...analytics import predict_probability

router = APIRouter(prefix='/predict', tags=['predictive-analytics'])

@router.post('/case-outcome', response_model=PredictResponse)
def predict_case(req: PredictRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    prob, factors = predict_probability(req.case_facts)
    return {'probability_of_success': prob, 'factors': factors}
