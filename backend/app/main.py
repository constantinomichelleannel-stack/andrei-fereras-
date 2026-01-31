from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db import Base, engine
from .api.routes import auth as auth_routes
from .api.routes import docs as docs_routes
from .api.routes import files as files_routes
from .api.routes import search as search_routes
from .api.routes import predict as predict_routes
from .api.routes import strategy as strategy_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
def health():
        return {'status': 'ok'}

app.include_router(auth_routes.router)
app.include_router(docs_routes.router)
app.include_router(files_routes.router)
app.include_router(search_routes.router)
app.include_router(predict_routes.router)
app.include_router(strategy_routes.router)
