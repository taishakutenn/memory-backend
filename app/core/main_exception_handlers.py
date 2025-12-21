from fastapi import FastAPI

# Импортируем все выброшенные ошибки
from app.core.exceptions.user import UserAlreadyExists, UserNotFound
# Импортируем все обработчики ошибок
from app.core.exception_handlers.user import (user_already_exists_handler,
                                              user_not_found_handler)


# Функция, которая зарегестрирует все обработчики ошибок в fastApi
def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
    app.add_exception_handler(UserNotFound, user_not_found_handler)
