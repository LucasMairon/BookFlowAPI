from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.db_config import get_session
from src.models.user import User
from src.models.token import Token
from src.utils.security import create_acess_token, verify_password

token_router = APIRouter(prefix='/token', tags=['token'])


@token_router.post('/', response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = await session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid email or password',
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid email or password',
        )

    access_token = create_acess_token({'sub': user.email})

    new_token = Token(
        access_token=access_token,
        token_type='Bearer',
    )

    return new_token
