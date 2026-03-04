import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key, default=None):
    value = os.getenv(key)
    return value if value not in (None, "") else default


def get_database_url():
    user = get_env("DB_USER", "root")
    password = get_env("DB_PASSWORD", "")
    host = get_env("DB_HOST", "127.0.0.1")
    port = get_env("DB_PORT", "3306")
    name = get_env("DB_NAME", "personal")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


def get_embedding_model():
    return get_env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
