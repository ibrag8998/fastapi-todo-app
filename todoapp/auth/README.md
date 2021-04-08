# Авторизация

## Использование

Функция ниже не сработает, если текущий пользователь не залогинен.

```python
@r.get('/items', dependencies=[Depends(get_current_user)])
def read_items():
    ...
```

Функция ниже отличается от верхней тем, что она получает текущего пользователя.

```python
@r.get('/items')
def read_items(user: User = Depends(get_current_user)):
    ...
```
