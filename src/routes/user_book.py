from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.db_config import get_session
from src.models.user import User
from src.models.user_book import UserBook
from src.routes.user import get_current_user
from src.schemas.user_book import (
    UserBookItensPublic,
    UserBookList,
    UserBookPartialUpdateSchema,
    UserBookPublic,
    UserBookSchema,
    UserBookUpdateSchema,
)
from src.utils.book import get_book_or_http_exception
from src.utils.user import verify_if_is_user_have_permission
from src.utils.user_book import get_user_book_or_http_404

user_book_router = APIRouter(prefix='/user_books', tags=['user_books'])


@user_book_router.post(
    path='/',
    response_model=UserBookPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_user_book(
    user_book: UserBookSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):

    verify_if_is_user_have_permission(user.id, user_book.user_id)
    get_book_or_http_exception(session, user_book.book_id)

    user_book = UserBook(**user_book.model_dump())
    session.add(user_book)
    session.commit()
    session.refresh(user_book)

    return user_book


@user_book_router.get(
    path='/', response_model=UserBookList, status_code=status.HTTP_200_OK
)
def get_user_books_by_logged_user(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user_books = session.scalars(
        select(UserBook).where(UserBook.user_id == user.id)
    ).all()
    return {'user_books': db_user_books}


@user_book_router.delete(
    path='/{user_book_id}', status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_book(
    user_book_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user_book = get_user_book_or_http_404(session, user_book_id)
    verify_if_is_user_have_permission(db_user_book.user_id, user.id)

    session.delete(db_user_book)
    session.commit()


@user_book_router.put(
    path='/{user_book_id}',
    response_model=UserBookItensPublic,
    status_code=status.HTTP_200_OK,
)
def update_user_book(
    user_book_id: int,
    user_book_data: UserBookUpdateSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user_book = get_user_book_or_http_404(session, user_book_id)
    verify_if_is_user_have_permission(db_user_book.user_id, user.id)

    for field, value in user_book_data.model_dump().items():
        setattr(db_user_book, field, value)

    session.commit()
    session.refresh(db_user_book)

    return db_user_book


@user_book_router.patch(
    path='/{user_book_id}',
    response_model=UserBookItensPublic,
    status_code=status.HTTP_200_OK,
)
def partial_update_user_book(
    user_book_id: int,
    user_book_data: UserBookPartialUpdateSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user_book = get_user_book_or_http_404(session, user_book_id)
    verify_if_is_user_have_permission(db_user_book.user_id, user.id)

    updated_data = {
        key: value
        for key, value in user_book_data.model_dump(exclude_unset=True).items()
    }

    for field, value in updated_data.items():
        setattr(db_user_book, field, value)
    session.commit()
    session.refresh(db_user_book)

    return db_user_book
