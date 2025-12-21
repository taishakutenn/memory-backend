from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.user import User


class UserRepository:
    async def create_user(self, db: AsyncSession, nickname: str, email: str, hashed_password: str):
        user = User(nickname=nickname, email=email, hashed_password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        result = await db.execute(select(User).where(User.nickname == nickname))
        user = result.scalar_one_or_none()
        return user

    async def get_all_users(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return list(users)
