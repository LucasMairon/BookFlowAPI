import sqlalchemy as sa
from .db_config import Base


class Book(Base):
    __tablename__ = "books"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    cover_url = sa.Column(sa.String, nullable=False)
