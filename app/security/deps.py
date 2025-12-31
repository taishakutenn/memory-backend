from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.db.user import User
from app.services.user import UserService
from app.config import ALGORITHM, SECRET_KEY
from app.security.exceptions import CredentialsException, InactiveUser
from app.security.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db)
    ):

    """Получение текущего пользователя из токена"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Вернем пользователя, зашитого в ключе
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException

        # Сериализуем имя пользователя моделью Pydantic
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CredentialsException

    # Пытаемся получить данные пользователя из базы
    user_service = UserService()
    user = await user_service.get_user_by_nickname(db, token_data.username)
    if user is None:
        raise CredentialsException

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Проверяет запись пользователя по полю `disabled`"""
    if current_user.disabled:
        raise InactiveUser
    return current_user