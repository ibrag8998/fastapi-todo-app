from fastapi import FastAPI

from todoapp.auth import auth
from todoapp.db.base import init_db

app = FastAPI()

# init database
init_db()

# include the routers
app.include_router(auth.r)

# load the playground for debug purposes
from todoapp import playground  # noqa
