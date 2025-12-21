from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.user import User
from app.security.security import get_password_hash, verify_password
from app.core.exceptions.user import UserAlreadyExists, UserNotFound, InvalidCredentials
from app.repositories.user import UserRepository


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def create_user(self, db: AsyncSession, nickname: str, email: str, password: str) -> User:
        # Проверяем, существует ли пользователь с таким email или nickname
        is_user_email = await self.user_repo.get_user_by_email(db, email)
        is_user_nickname = await self.user_repo.get_user_by_nickname(db, nickname)
        if is_user_email or is_user_nickname:
            raise UserAlreadyExists()

        # Преобразовываем данные перед отправкой в репозитории
        hashed_password = get_password_hash(password)
        # Создаём его в бд
        user = await self.user_repo.create_user(db, nickname, email, hashed_password)
        return user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        user = await self.user_repo.get_user_by_email(db, email)
        if user is None:
            raise UserNotFound()
        return user

    async def get_all_users(self, db: AsyncSession):
        users = await self.user_repo.get_all_users(db)
        return users
