import sqlalchemy as sa
import uuid

from src.models.db_config import Base


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(
        sa.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    email = sa.Column(sa.String(50), nullable=False, index=True, unique=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
