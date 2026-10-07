import uuid
from sqlmodel import Field, SQLModel


class BookBase(SQLModel):
    title: str = Field(nullable=False, index=True)
    author: str = Field(nullable=False, index=True)
    cover_url: str = Field(nullable=False)


class BookCreate(BookBase):
    pass


class BookPartialUpdate(SQLModel):
    title: str | None = Field(index=True)
    author: str | None = Field(index=True)
    cover_url: str | None = None


class BookPublic(BookBase):
    id: uuid.UUID


class BookList(SQLModel):
    books: list[BookPublic]


class Book(BookBase, table=True):
    __tablename__ = 'books'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
