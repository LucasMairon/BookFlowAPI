import sqlalchemy as sa
from .db_config import Base


class Book(Base):
    __tablename__ = "books"
    id = sa.Column(sa.Integer, primary_key=True,
                   autoincrement=True, index=True)
    title = sa.Column(sa.String, nullable=False, index=True)
    author = sa.Column(sa.String, nullable=False, index=True)
    cover_url = sa.Column(sa.String, nullable=False)
