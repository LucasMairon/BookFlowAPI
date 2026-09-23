import enum

import sqlalchemy as sa

from src.models.db_config import Base


class StatusChoices(enum.Enum):
    READING = 'reading'
    WANT_TO_READ = 'want_to_read'
    FINISHED = 'finished'


class UserBook(Base):
    __tablename__ = 'user_books'
    id = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True, index=True
    )
    status = sa.Column(sa.Enum(StatusChoices), nullable=True)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    book_id = sa.Column(sa.Integer, sa.ForeignKey('books.id'), nullable=False)
