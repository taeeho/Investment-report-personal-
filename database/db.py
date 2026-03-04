from sqlalchemy import create_engine
from utils.config import get_database_url


engine = create_engine(get_database_url(), pool_pre_ping=True)
