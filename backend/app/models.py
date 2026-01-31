from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
from pgvector.sqlalchemy import Vector
from .core.config import settings

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    tags = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    uploaded_by = relationship('User')
    file_path = Column(String(512), nullable=True)
    mime_type = Column(String(100), nullable=True)

class DocChunk(Base):
    __tablename__ = 'doc_chunks'
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey('documents.id'), index=True)
    chunk_index = Column(Integer)
    content = Column(Text)
    embedding = Column(Vector(dim=settings.EMBEDDING_DIM))

class CaseRecord(Base):
    __tablename__ = 'case_records'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    facts = Column(Text)
    outcome = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(255))
    entity = Column(String(255))
    entity_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
