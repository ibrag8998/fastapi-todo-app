import sys

from fastapi import FastAPI

from todoapp.db.base import init_db

app = FastAPI()


@app.get('/')
def index():
    return {"message": "hello"}


# at the end
init_db()

# load the playground
from todoapp import playground  # noqa
