import sqlalchemy as sa
from sqlalchemy import orm

from todoapp.config import settings


@orm.as_declarative()
class Base:
    id = sa.Column(sa.Integer, primary_key=True)


def create_all_tables():  # для экспорта
    Base.metadata.create_all(engine)


engine = sa.create_engine(settings.DB_URL, echo=settings.DEBUG)
Session = orm.sessionmaker(bind=engine)
