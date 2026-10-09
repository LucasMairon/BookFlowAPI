import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.db_config import get_session
from src.models.user import (
    User,
    UserCreate,
    UserList,
    UserPartialUpdate,
    UserPublic,
    UserUpdate,
)
from src.utils.security import (
    get_password_hash,
)
from src.utils.user import (
    verify_if_is_user_have_permission,
    verify_if_user_exist,
)

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

user_router = APIRouter(prefix='/users', tags=['users'])


@user_router.get(
    path='{user_id}/',
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, os.getenv('SECRET_KEY'), os.getenv('ALGORITHM')
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = await session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user


@user_router.get(
    path='/', response_model=UserList, status_code=status.HTTP_200_OK
)
async def list_users(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 20,
    user: User = Depends(get_current_user),
):
    query = await session.scalars(select(User).offset(offset).limit(limit))
    users = query.all()

    return {'users': users}


@user_router.post(
    path='/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def singup(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    await session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@user_router.delete(path='/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user = session.get(User, user_id)
    verify_if_is_user_have_permission(user_id, user.id)
    verify_if_user_exist(db_user)

    await session.delete(db_user)
    await session.commit()


@user_router.put(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user = await session.get(User, user_id)
    verify_if_is_user_have_permission(user_id, user.id)
    verify_if_user_exist(db_user)

    data_to_update = user_data.model_dump()

    raw_password = data_to_update.pop('password')
    db_user.hashed_password = get_password_hash(raw_password)

    for field, value in data_to_update.items():
        setattr(db_user, field, value)

    await session.commit()
    await session.refresh(db_user)

    return db_user


@user_router.patch(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
async def partial_update_user(
    user_id: UUID,
    user_data: UserPartialUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_user = await session.get(User, user_id)
    verify_if_is_user_have_permission(user_id, user.id)
    verify_if_user_exist(db_user)

    data_to_update = user_data.model_dump(exclude_unset=True)

    if 'password' in data_to_update:
        raw_password = data_to_update.pop('password')
        db_user.hashed_password = get_password_hash(raw_password)

    updated_data = {key: value for key, value in data_to_update.items()}

    for field, value in updated_data.items():
        setattr(db_user, field, value)

    await session.commit()
    await session.refresh(db_user)

    return db_user
