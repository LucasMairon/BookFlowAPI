import enum
import uuid

from sqlmodel import Field, Relationship, SQLModel

from src.models.book import Book, BookPublic
from src.models.user import User, UserPublic


class StatusChoices(enum.Enum):
    READING = 'reading'
    WANT_TO_READ = 'want_to_read'
    FINISHED = 'finished'


class UserBookBase(SQLModel):
    status: StatusChoices = Field(nullable=False, index=True)


class UserBookUpdate(UserBookBase):
    pass


class UserBookPartialUpdate(SQLModel):
    status: StatusChoices = Field(nullable=True, index=True)


class UserBookCreate(UserBookBase):
    user_id: uuid.UUID = Field(nullable=False, foreign_key='users.id')
    book_id: uuid.UUID = Field(nullable=False, foreign_key='books.id')


class UserBookPublic(UserBookBase):
    id: uuid.UUID = Field(nullable=False)
    user: UserPublic
    book: BookPublic


class UserBookItensPublic(UserBookBase):
    id: uuid.UUID = Field(nullable=False)
    book: BookPublic


class UserBookList(SQLModel):
    user_books: list[UserBookItensPublic]


class UserBook(UserBookBase, table=True):
    __tablename__ = 'user_books'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        nullable=False, foreign_key='users.id', ondelete='CASCADE'
    )
    book_id: uuid.UUID = Field(nullable=False, foreign_key='books.id')

    book: Book = Relationship()
    user: User = Relationship()
