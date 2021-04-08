import os
from datetime import timedelta


def router(name: str) -> str:
    return f'{name}.routes.{name}_router'


PACKAGE_NAME = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[-1]

DEBUG = bool(os.environ.get('DEBUG', False))

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRET_KEY', 'e8942d10de0e5503b53500bf94ba5a2551fee96ac3c07b0c2967a994bf70b2c4')

DB_URL = os.environ.get('DB_URL', 'sqlite:///db.sqlite3')

ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
if DEBUG:
    ACCESS_TOKEN_EXPIRES = timedelta(days=30)

AUTH_JWT_ALGORITHM = "HS256"

MODELS_MODULES = [
    'users.models',
    'todos.models',
]

ROUTERS = [
    # 'auth.routes.auth_router',
    router('auth'),
]
