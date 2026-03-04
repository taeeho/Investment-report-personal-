import json
import numpy as np
from sqlalchemy import text
from database.db import engine


def _cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def search_similar(query_embedding, company, limit=5):
    if not query_embedding:
        return []
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                """
                SELECT title, link, published, content, embedding
                FROM news_embeddings
                WHERE company = :company
                """
            ),
            {"company": company},
        ).fetchall()
    scored = []
    for row in rows:
        try:
            emb = json.loads(row[4])
        except Exception:
            emb = None
        if not emb:
            continue
        score = _cosine_similarity(query_embedding, emb)
        scored.append((score, row))
    scored.sort(key=lambda item: item[0], reverse=True)
    results = []
    for _, row in scored[:limit]:
        results.append(
            {
                "title": row[0],
                "link": row[1],
                "published": row[2],
                "summary": row[3],
            }
        )
    return results
