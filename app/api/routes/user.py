from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.user import UserCreate, UserShow
from app.services.user import UserService

user_router = APIRouter()


@user_router.post("/create", response_model=UserShow)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService()
    user = await service.create_user(db, body.nickname, body.email, body.password)
    return user


@user_router.get("/search/all", response_model=list[UserShow])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    service = UserService()
    users = await service.get_all_users(db)
    return users


@user_router.get("/search/by-email/{email}", response_model=UserShow)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    service = UserService()
    user = await service.get_user_by_email(db, email)
    return user


