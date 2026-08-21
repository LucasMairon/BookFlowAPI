from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.book import Book
from src.models.db_config import get_session
from src.schemas.book import (
    BookList,
    BookPartialUpdate,
    BookPublic,
    BookSchema,
)
from src.utils.book import get_book_or_http_exception

book_router = APIRouter(prefix='/books', tags=['books'])


@book_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=BookList,
)
def list_books(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 30
):
    query = session.scalars(select(Book).offset(offset).limit(limit))
    books = query.all()

    return {'books': books}


@book_router.post(
    path='/',
    response_model=BookPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookSchema, session: Session = Depends(get_session)):
    book = Book(**book.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@book_router.get(
    path='/{book_id}',
    response_model=BookPublic,
    status_code=status.HTTP_200_OK,
)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = get_book_or_http_exception(session, book_id)

    return book


@book_router.delete(
    path='/delete/{book_id}', status_code=status.HTTP_204_NO_CONTENT
)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = get_book_or_http_exception(session, book_id)
    session.delete(book)
    session.commit()


@book_router.put(
    path='/{book_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookPublic,
)
def update_book(
    book_id: int, book: BookSchema, session: Session = Depends(get_session)
):
    db_book = get_book_or_http_exception(session, book_id)

    for field, value in book.model_dump().items():
        setattr(db_book, field, value)
        session.commit()
        session.refresh(db_book)

    return db_book


@book_router.patch(
    path='/{book_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=BookPublic,
)
def partial_update_book(
    book_id: int,
    book: BookPartialUpdate,
    session: Session = Depends(get_session),
):
    db_book = get_book_or_http_exception(session, book_id)

    updated_data = {
        key: value
        for key, value in book.model_dump(exclude_unset=True).items()
    }
    for field, value in updated_data.items():
        setattr(db_book, field, value)
    session.commit()
    session.refresh(db_book)

    return db_book
