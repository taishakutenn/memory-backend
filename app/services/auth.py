from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.security.jwt import authenticate_user, create_access_token
from app.security.exceptions import UserUnauthorized
from app.security.schemas import Token


class AuthService:
    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm, db: AsyncSession):
        # Проходим проверку подлинности
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise UserUnauthorized

        # Устанавливаем время жизни токена
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # Генерируем токен доступа
        access_token = await create_access_token(
            data={"sub": user.nickname}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")