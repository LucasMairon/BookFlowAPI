from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.user_book import StatusChoices
from src.schemas.book import BookPublic
from src.schemas.user import UserPublic


class UserBookSchema(BaseModel):
    status: StatusChoices
    user_id: UUID
    book_id: UUID


class UserBookUpdateSchema(BaseModel):
    status: StatusChoices


class UserBookPartialUpdateSchema(BaseModel):
    status: Optional[StatusChoices]


class UserBookPublic(BaseModel):
    id: UUID
    status: StatusChoices
    user: UserPublic
    book: BookPublic

    model_config = ConfigDict(from_attributes=True)


class UserBookItensPublic(BaseModel):
    id: UUID
    status: StatusChoices
    book: BookPublic

    model_config = ConfigDict(from_attributes=True)


class UserBookList(BaseModel):
    user_books: list[UserBookItensPublic]
