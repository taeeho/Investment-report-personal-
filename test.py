from sqlalchemy import text
from database.db import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.fetchone())
except Exception as e:
    print("DB 연결 오류:", e)