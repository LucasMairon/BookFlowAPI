from sqlmodel import SQLModel


class Token(SQLModel):
    token_type: str
    access_token: str
