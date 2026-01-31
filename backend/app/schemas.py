from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class DocumentIn(BaseModel):
    title: str
    tags: Optional[str] = None

class DocumentOut(DocumentIn):
    id: int
    created_at: datetime
    file_path: Optional[str] = None
    mime_type: Optional[str] = None
    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)

class SearchHit(BaseModel):
    doc_id: int
    title: str
    score: float
    snippet: str

class PredictRequest(BaseModel):
    case_facts: str

class PredictResponse(BaseModel):
    probability_of_success: float
    factors: List[str] = []

class StrategyRequest(BaseModel):
    objective: str
    case_facts: str

class StrategySuggestion(BaseModel):
    label: str
    rationale: str
    references: List[str] = []

class StrategyResponse(BaseModel):
    suggestions: List[StrategySuggestion]
