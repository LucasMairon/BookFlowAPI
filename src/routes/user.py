from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.db_config import get_session
from src.models.user import User
from src.schemas.user import Token, UserPublic, UserSchema
from src.utils.security import get_password_hash, verify_password
from src.utils.security import create_acess_token

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


@user_router.post(
    '/token',
    response_model=Token,
)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.email == form_data.username)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid email or password'
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid email or password'
        )

    acess_token = create_acess_token(
        {'sub': user.email}
    )

    new_token = Token(
        acess_token=acess_token,
        token_type='Bearer',
    )

    return new_token
