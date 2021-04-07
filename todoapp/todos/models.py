from datetime import datetime

import sqlalchemy as sa

from ..db.base import Base


class Todo(Base):
    __tablename__ = 'todos'
    
    title = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime, default=datetime.now())

    def __init__(self, title: str, desciption: str, **kwargs) -> None:
        self.title = title
        self.description = desciption
