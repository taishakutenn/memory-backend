from fastapi import FastAPI

# User
# Импортируем все выброшенные ошибки
from app.core.exceptions.user import UserAlreadyExists, UserNotFound
# Импортируем все обработчики ошибок
from app.core.exception_handlers.user import (user_already_exists_handler,
                                              user_not_found_handler)

# Auth
from app.security.exceptions import CredentialsException, InactiveUser, UserUnauthorized, AccessDenied
from app.security.exception_handlers import credentials_exception, inactive_user, user_unauthorized, access_denied

# Note
from app.core.exceptions.note import NoteNotFound
from app.core.exception_handlers.note import note_not_found_handler

# GroupTask
from app.core.exceptions.group_task import GroupTaskNotFound
from app.core.exception_handlers.group_task import group_task_not_found_handler


# Функция, которая зарегестрирует все обработчики ошибок в fastApi
def register_exception_handlers(app: FastAPI) -> None:
    # User
    app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
    app.add_exception_handler(UserNotFound, user_not_found_handler)

    # Auth
    app.add_exception_handler(CredentialsException, credentials_exception)
    app.add_exception_handler(InactiveUser, inactive_user)
    app.add_exception_handler(UserUnauthorized, user_unauthorized)
    app.add_exception_handler(AccessDenied, access_denied)

    # Note
    app.add_exception_handler(NoteNotFound, note_not_found_handler)

    # GroupTask
    app.add_exception_handler(GroupTaskNotFound, group_task_not_found_handler)
