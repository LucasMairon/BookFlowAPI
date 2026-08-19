from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.book import Book
from src.models.db_config import get_session
from src.schemas.book import BookList, BookPublic, BookSchema

from ..utils.search_books import get_cleaned_books_list

BOOK_API_SEARCH_URL = "https://openlibrary.org/"

book_router = APIRouter(
    prefix='/books',
    tags=['books']
)


@book_router.get(
    path='{search_term}',
    status_code=status.HTTP_200_OK,
)
def book_search(search_term: str | None = None, page: str | None = None):
    search_url = f'{BOOK_API_SEARCH_URL}search.json'

    if search_term is not None:
        clean_search_term = search_term.replace(" ", "+")
        url_params = {
            'q': clean_search_term,
            'fields': ['author_name', 'cover_i', 'title', 'edit_count'],
            'lang': 'pt-BR',
            'offset': 0,
            'limit': 30,
            'page': page,
        }

    books = get_cleaned_books_list(search_url, url_params)

    return books


@book_router.post(
    path='/',
    response_model=BookPublic,
    status_code=status.HTTP_201_CREATED,
)
def book_create(book: BookSchema, session: Session = Depends(get_session)):
    book = Book(**book.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@book_router.get(
    path='/',
    response_model=BookList,
    status_code=status.HTTP_200_OK
)
def book_list(session: Session = Depends(get_session), offsett: int = 0, limit: int = 30):
    query = session.scalars(select(Book).offset(offsett).limit(limit))
    books = query.all()

    return {'books': books}


@book_router.get(
    path='/{book_id}',
    response_model=BookPublic,
    status_code=status.HTTP_200_OK
)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found',
        )

    return book


@book_router.delete(
    path='/delete/{book_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    session.delete(book)
    session.commit()


@book_router.put(
    path='/{book_id}',
    status_code=status.HTTP_200_OK,
    response_model=BookPublic
)
def update_book(
    book_id: int,
    book: BookSchema,
    session: Session = Depends(get_session)
):
    db_book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )

    for field, value in book.model_dump().items():
        setattr(db_book, field, value)
        session.commit()
        session.refresh(db_book)

    return db_book
