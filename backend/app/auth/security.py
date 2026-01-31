from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from ..core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(subject: str, expires_minutes: Optional[int] = None):
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {'sub': subject, 'exp': expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
