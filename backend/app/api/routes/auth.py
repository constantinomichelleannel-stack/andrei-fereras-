from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...schemas import UserCreate, UserOut, Token
from ...models import User
from ...auth.security import get_password_hash, verify_password, create_access_token
from ..deps import get_db

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(email=user_in.email, full_name=user_in.full_name, hashed_password=get_password_hash(user_in.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post('/login', response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    token = create_access_token(subject=user.email)
    return {'access_token': token}
