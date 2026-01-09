from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.db.user import User
from app.schemas.user import UserCreate, UserShow, PatchUserNickname
from app.security.deps import get_current_active_user
from app.services.user import UserService

user_router = APIRouter()


@user_router.post("/create", response_model=UserShow)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService()
    user = await service.create_user(db, body)
    return user


@user_router.get("/search/all", response_model=list[UserShow])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    service = UserService()
    users = await service.get_all_users(db)
    return users


@user_router.get("/search/by-email/{email}", response_model=UserShow)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_active_user)):
    service = UserService()
    user = await service.get_user_by_email(db, email)
    return user


@user_router.get("/search/by-nickname/{nickname}", response_model=UserShow)
async def get_user_by_nickname(nickname: str, db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_active_user)):
    service = UserService()
    user = await service.get_user_by_nickname(db, nickname)
    return user


@user_router.patch("/patch/nickname", response_model=UserShow)
async def patch_user_nickname(body: PatchUserNickname, db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_active_user)):
    service = UserService()
    # Передаём текущего пользователя полностью
    patched_user = await service.patch_user_nickname(db, current_user, body.nickname)
    return patched_user


@user_router.delete("/delete/me")
async def delete_current_user(db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_active_user)):
    service = UserService()
    deleted_user = await service.delete_user(db, current_user.uuid) # True/False
    return deleted_user
