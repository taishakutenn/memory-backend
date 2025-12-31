from pydantic import EmailStr

from app.schemas import TuneModel


class UserCreate(TuneModel):
    nickname: str
    email: EmailStr
    password: str


class UserShow(TuneModel):
    nickname: str
    email: EmailStr
    disabled: bool | None = None


class UserInDb(UserShow):
    hashed_password: str
