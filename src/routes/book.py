from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.book import (
    Book,
    BookCreate,
    BookList,
    BookPartialUpdate,
    BookPublic,
)
from src.models.db_config import get_session
from src.models.user import User
from src.routes.user import get_current_user
from src.utils.book import get_book_or_http_exception

book_router = APIRouter(prefix='/books', tags=['books'])


@book_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=BookList,
)
async def list_books(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 30
):
    query = await session.scalars(select(Book).offset(offset).limit(limit))
    books = query.all()

    return {'books': books}


@book_router.post(
    path='/',
    response_model=BookPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    book = Book(**book.model_dump())
    await session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


@book_router.get(
    path='/{book_id}',
    response_model=BookPublic,
    status_code=status.HTTP_200_OK,
)
async def get_book(book_id: UUID, session: Session = Depends(get_session)):
    book = await get_book_or_http_exception(session, book_id)

    return book


@book_router.delete(
    path='/delete/{book_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_id: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    book = await get_book_or_http_exception(session, book_id)
    await session.delete(book)
    await session.commit()


@book_router.put(
    path='/{book_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookPublic,
)
async def update_book(
    book_id: UUID,
    book: BookCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_book = await get_book_or_http_exception(session, book_id)

    for field, value in book.model_dump().items():
        setattr(db_book, field, value)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@book_router.patch(
    path='/{book_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=BookPublic,
)
async def partial_update_book(
    book_id: UUID,
    book: BookPartialUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_book = await get_book_or_http_exception(session, book_id)

    updated_data = {
        key: value
        for key, value in book.model_dump(exclude_unset=True).items()
    }
    for field, value in updated_data.items():
        setattr(db_book, field, value)
    await session.commit()
    await session.refresh(db_book)

    return db_book
