from sqlalchemy.orm import Session
from sqlalchemy import text
from .models import DocChunk, Document
from .embeddings import embed_texts
from typing import List, Tuple

def index_document_chunks(db: Session, doc: Document, chunks: List[str]):
    if not chunks:
        return
    embs = embed_texts(chunks)
    for i, (c, e) in enumerate(zip(chunks, embs)):
        row = DocChunk(doc_id=doc.id, chunk_index=i, content=c, embedding=e)
        db.add(row)
    db.commit()

def semantic_search(db: Session, query: str, top_k: int = 10) -> List[Tuple[int, str, float, str]]:
    q_emb = embed_texts([query])[0]
    sql = text('SELECT dc.doc_id, d.title, (dc.embedding <#> :q)::float AS distance, dc.content '
               'FROM doc_chunks dc JOIN documents d ON d.id = dc.doc_id '
               'ORDER BY dc.embedding <#> :q LIMIT :k')
    rows = db.execute(sql, {'q': q_emb, 'k': top_k}).fetchall()
    results = []
    for r in rows:
        score = float(1.0 - r.distance)
        snippet = (r.content or '')[:220].replace('
', ' ')
        results.append((int(r.doc_id), r.title or f'Document {r.doc_id}', score, snippet))
    return results
