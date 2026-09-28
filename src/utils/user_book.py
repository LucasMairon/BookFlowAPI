from fastapi import HTTPException, status

from src.models.user_book import UserBook


def get_user_book_or_http_404(session, user_book_id):
    db_user_book = session.get(UserBook, user_book_id)
    if not db_user_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='user_book not found'
        )

    return db_user_book
