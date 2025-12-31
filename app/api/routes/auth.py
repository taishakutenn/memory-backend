from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.user import UserCreate, UserShow
from app.security.jwt import authenticate_user
from app.security.schemas import Token
from app.services.auth import AuthService

auth_router = APIRouter()


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: AsyncSession = Depends(get_db)):
    service = AuthService()
    token = await service.login_for_access_token(form_data, db)
    return token