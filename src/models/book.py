import sqlalchemy as sa
import uuid

from .db_config import Base


class Book(Base):
    __tablename__ = 'books'
    id = sa.Column(
        sa.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    title = sa.Column(sa.String, nullable=False, index=True)
    author = sa.Column(sa.String, nullable=False, index=True)
    cover_url = sa.Column(sa.String, nullable=False)
