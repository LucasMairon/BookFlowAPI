import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash
from dotenv import load_dotenv

pwd_context = PasswordHash.recommended()

load_dotenv()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_acess_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + \
        timedelta(minutes=int(os.getenv('ACESS_TOKEN_EXPIRE_MINUTES')))

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, os.getenv('SECRET_KEY'),
                         algorithm=os.getenv('ALGORITHM'))

    return encoded_jwt
