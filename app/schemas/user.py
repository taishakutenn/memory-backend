from pydantic import EmailStr
from uuid import UUID

from app.schemas import TuneModel


class UserCreate(TuneModel):
    nickname: str
    email: EmailStr
    password: str


class UserShow(TuneModel):
    nickname: str
    email: EmailStr
    disabled: bool | None = None


class MeShow(UserShow):
    uuid: UUID


class UserInDb(UserShow):
    hashed_password: str


class PatchUserNickname(TuneModel):
    nickname: str
