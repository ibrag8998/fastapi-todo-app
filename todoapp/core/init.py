from importlib import import_module

from fastapi import FastAPI

from ..config import settings
from ..db.base import create_all_tables


def init(app: FastAPI) -> None:
    init_db()
    init_routers(app)


def init_db() -> None:
    for models_module in settings.MODELS_MODULES:
        import_module(f'{settings.PACKAGE_NAME}.{models_module}')
    create_all_tables()


def init_routers(app: FastAPI) -> None:
    for router_path in settings.ROUTERS:
        path, _, router_name = router_path.rpartition('.')
        module = import_module(f'{settings.PACKAGE_NAME}.{path}')
        router = getattr(module, router_name)
        app.include_router(router)
