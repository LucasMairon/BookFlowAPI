import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, nullable=False)


class UserCreate(UserBase):
    password: str


class UserPartialUpdate(SQLModel):
    email: EmailStr | None = None


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool


class UserPublic(UserBase):
    id: uuid.UUID


class UserList(SQLModel):
    users: list[UserRead]


class User(UserBase, table=True):
    __tablename__ = 'users'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
