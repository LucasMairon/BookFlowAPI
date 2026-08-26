from fastapi import APIRouter, Depends, status
from src.models.db_config import get_session
from src.models.user import User
from src.schemas.user import UserSchema, UserPublic
from sqlalchemy.orm import Session
from src.utils.security import get_password_hash


user_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post(
    path='/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
def singup(user: UserSchema, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
