from src.models.book import Book
from fastapi import HTTPException, status


def get_book_or_http_exception(session, book_id):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )

    return book
