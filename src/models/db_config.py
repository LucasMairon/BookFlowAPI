from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = 'sqlite+aiosqlite:///./db.sqlite3'

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def get_session():
    async with async_session_maker() as session:
        yield session
