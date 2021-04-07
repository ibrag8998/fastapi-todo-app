import sqlalchemy as sa

from ..db.base import Base
from ..utils.hashing import check_password_hash, generate_password_hash


class User(Base):
    __tablename__ = 'users'

    username = sa.Column(sa.String(63), unique=True, nullable=False)
    password = sa.Column(sa.String(127), nullable=False)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.set_password(password)

    def set_password(self, raw: str) -> None:
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)
