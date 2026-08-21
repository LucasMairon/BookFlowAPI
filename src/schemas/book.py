from typing import Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    cover_url: str


class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    cover_url: str


class BookPartialUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None


class BookList(BaseModel):
    books: list[BookPublic]
