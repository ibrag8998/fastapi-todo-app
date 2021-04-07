import os

import sqlalchemy as sa
from sqlalchemy import orm
from todoapp.config import settings


class BaseModel:
    id = sa.Column(sa.Integer, primary_key=True)


def init_db():
    # import models
    from ..todos import models
    from ..users import models

    Base.metadata.create_all(engine)


engine = sa.create_engine(settings.DB_URL, echo=settings.DEBUG)
Base = orm.declarative_base(cls=BaseModel)
Session = orm.sessionmaker(bind=engine)
# Session = orm.scoped_session(orm.sessionmaker(bind=engine))
