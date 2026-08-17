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


class BookList(BaseModel):
    books: list[BookPublic]
