from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = 'PRAL Legal KM'
    ENV: str = 'dev'
    SECRET_KEY: str = 'change-me'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str = 'postgresql+psycopg2://pral:pralpwd@localhost:5432/pralkm'
    BACKEND_CORS_ORIGINS: List[str] = ['http://localhost:8080','http://127.0.0.1:8080']
    STORAGE_DIR: str = './storage'
    EMBEDDING_MODEL: str = 'sentence-transformers/all-MiniLM-L6-v2'
    EMBEDDING_DIM: int = 384

    class Config:
        env_file = '.env'

settings = Settings()
