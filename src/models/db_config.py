from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABSE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    DATABSE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
