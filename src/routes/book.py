import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.models.book import Book
from src.models.db_config import get_session
from src.schemas.book import BookPublic, BookSchema

from ..utils.search_books import get_cleaned_books_list

load_dotenv()

book_router = APIRouter(
    prefix='/books',
    tags=['books']
)


@book_router.get('/')
async def list_books(search_term: str | None = None):
    search_url = f'{os.getenv("BOOK_API_SEARCH_URL")}search.json'

    if search_term is not None:
        clean_search_term = search_term.replace(" ", "+")
        url_params = {
            'q': clean_search_term,
            'fields': '*',
            'lang': 'pt-BR',
        }

    books = get_cleaned_books_list(search_url, url_params)

    return {"listed_books": books}


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
