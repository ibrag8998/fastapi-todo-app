from icecream import ic
from sqlalchemy.exc import IntegrityError

from .db.base import Session
from .users.models import User

RUN = False
# RUN = True  # comment this line to toggle running

if RUN:
    s = Session()
    #

    admin = User(username='admin', password='admin')
    s.query(User).filter(User.username == 'admin').delete()
    s.add(admin)
    s.commit()

    #
    s.close()
