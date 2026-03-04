import json
from sqlalchemy import text
from database.db import engine


def store_embeddings(company, news_list, embeddings):
    if not news_list or not embeddings:
        return 0
    if len(news_list) != len(embeddings):
        return 0
    rows = []
    for item, emb in zip(news_list, embeddings):
        rows.append(
            {
                "company": company,
                "title": item.get("title"),
                "link": item.get("link"),
                "published": item.get("published"),
                "content": item.get("summary"),
                "embedding": json.dumps(emb),
            }
        )
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO news_embeddings
                (company, title, link, published, content, embedding)
                VALUES
                (:company, :title, :link, :published, :content, :embedding)
                """
            ),
            rows,
        )
    return len(rows)
