from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookSchema(BaseModel):
    title: str
    author: str
    cover_url: str


class BookPublic(BaseModel):
    id: UUID
    title: str
    author: str
    cover_url: str

    model_config = ConfigDict(from_attributes=True)


class BookPartialUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None


class BookList(BaseModel):
    books: list[BookPublic]
