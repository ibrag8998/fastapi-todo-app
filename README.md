# Todo App

## Запуск

```shell
# create venv
python -m venv venv
# activate venv
& venv/Scripts/activate # for windows
. venv/bin/activate # for linux
# install dependencies
pip install -r requirements.txt
# run in debug mode with autoreload
uvicorn --reload app:app
```
