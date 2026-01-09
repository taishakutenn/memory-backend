from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.user import User
from app.security.password import get_password_hash
from app.core.exceptions.user import UserAlreadyExists, UserNotFound
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def _get_user_by_nickname_email(self, db: AsyncSession, nickname: str, email: str) -> User | None:
        user = await self.user_repo.get_user_by_nickname_or_email(db, nickname, email)
        return user

    async def create_user(self, db: AsyncSession, data: UserCreate) -> User:
        # Проверяем, существует ли пользователь с таким email или nickname
        is_user = await self._get_user_by_nickname_email(db, data.nickname, data.email)
        if is_user:
            raise UserAlreadyExists()

        # Преобразовываем данные перед отправкой в репозитории
        hashed_password = get_password_hash(data.password)
        # Создаём его
        user = User(
            nickname=data.nickname,
            email=data.email,
            hashed_password=hashed_password
        )

        # Сохраняем в бд использую репозитории
        user = await self.user_repo.create_user(db, user)
        return user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        user = await self.user_repo.get_user_by_email(db, email)
        if user is None:
            raise UserNotFound()
        return user

    async def get_user_by_nickname(self, db: AsyncSession, nickname: str) -> User:
        user = await self.user_repo.get_user_by_nickname(db, nickname)
        if user is None:
            raise UserNotFound()
        return user

    async def get_all_users(self, db: AsyncSession):
        users = await self.user_repo.get_all_users(db)
        return users

    async def patch_user_nickname(self, db: AsyncSession, user: User, new_user_nickname: str) -> User:
        # Проверяем, не занят ли новый ник
        existing_user = await self.user_repo.get_user_by_nickname(db, new_user_nickname)
        if existing_user:
            raise UserAlreadyExists()

        # Проверяем, что новый ник отличается от старого
        if user.nickname == new_user_nickname:
            return user

        # Обновляем юзеру никнейм
        user.nickname = new_user_nickname
        patched_user = await self.user_repo.patch_user_nickname(db, user)
        return patched_user

    async def delete_user(self, db: AsyncSession, user_uuid: UUID) -> bool:
        deleted_user = await self.user_repo.delete_user(db, user_uuid)
        return deleted_user

