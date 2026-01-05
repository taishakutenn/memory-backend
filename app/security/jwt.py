from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from typing import Annotated

import jwt
from fastapi import Depends
from jwt import InvalidTokenError

from app.db import get_db
from app.db.user import User
from app.services.user import UserService
from app.config import ALGORITHM, SECRET_KEY
from app.security.password import verify_password
from app.security.exceptions import CredentialsException
from app.security.schemas import TokenData

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta, timezone


async def authenticate_user(db: AsyncSession, nickname: str, password: str) -> User | bool:
    """Функция для проверки подлинности пользователя"""
    user_service = UserService()

    user = await user_service.get_user_by_nickname(db, nickname)
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Служебная функция для генерации нового токена"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

