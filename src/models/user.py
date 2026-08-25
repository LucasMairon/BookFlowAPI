import sqlalchemy as sa

from src.models.db_config import Base


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True, index=True
    )
    email = sa.Column(
        sa.String(50), nullable=False, index=True, unique=True
    )
    hashed_password = sa.Column(
        sa.String, nullable=False
    )
    is_active = sa.Column(
        sa.Boolean, default=True
    )
