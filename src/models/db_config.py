from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABSE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    DATABSE_URL
)

Base = declarative_base()
