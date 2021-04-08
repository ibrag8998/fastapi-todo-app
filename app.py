from fastapi import FastAPI

from todoapp.core.init import init

app = FastAPI()

init(app)

# load the playground for debug purposes
from todoapp import playground  # noqa
