from sqlalchemy import text
from database.db import engine


def create_tables():
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS news_embeddings (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    company TEXT NOT NULL,
                    title TEXT,
                    link TEXT,
                    published TEXT,
                    content TEXT,
                    embedding LONGTEXT
                )
                """
            )
        )


if __name__ == "__main__":
    create_tables()
