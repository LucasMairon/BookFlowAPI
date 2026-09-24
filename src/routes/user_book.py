from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.models.db_config import get_session
from src.models.user import User
from src.models.user_book import UserBook
from src.routes.user import get_current_user
from src.schemas.user_book import UserBookPublic, UserBookSchema
from src.utils.book import get_book_or_http_exception
from src.utils.user import verify_if_is_user_have_permission

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
