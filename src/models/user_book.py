import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.models.db_config import Base


class StatusChoices(enum.Enum):
    READING = 'reading'
    WANT_TO_READ = 'want_to_read'
    FINISHED = 'finished'


class UserBook(Base):
    __tablename__ = 'user_books'
    id = sa.Column(
        sa.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4,  index=True
    )
    status = sa.Column(sa.Enum(StatusChoices), nullable=True)
    user_id = sa.Column(
        sa.Uuid(as_uuid=True),
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    book_id = sa.Column(sa.Uuid(as_uuid=True),
                        sa.ForeignKey('books.id'), nullable=False)
    user = relationship('User')
    book = relationship('Book')
