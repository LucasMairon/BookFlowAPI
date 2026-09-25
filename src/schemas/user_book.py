from pydantic import BaseModel, ConfigDict

from src.models.user_book import StatusChoices
from src.schemas.book import BookPublic
from src.schemas.user import UserPublic


class UserBookSchema(BaseModel):
    status: StatusChoices
    user_id: int
    book_id: int


class UserBookPublic(BaseModel):
    id: int
    status: StatusChoices
    user: UserPublic
    book: BookPublic

    model_config = ConfigDict(from_attributes=True)


class UserBookItensPublic(BaseModel):
    id: int
    status: StatusChoices
    book: BookPublic

    model_config = ConfigDict(from_attributes=True)


class UserBookList(BaseModel):
    user_books: list[UserBookItensPublic]
