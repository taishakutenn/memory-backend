import uuid
import bcrypt

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = mapped_column(String(20), uinque=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True)

    # Взаимосвязи с другими таблицами
    ...

    def set_password(self, password: str) -> None:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode("utf-8")
        hash_bytes = bcrypt.hashpw(pwd_bytes, salt)

        self.hashed_password = hash_bytes.decode("utf-8")

    def verify_password(self, password: str) -> bool:
        if self.hashed_password is None:
            return False

        pwd_bytes = password.encode("utf-8")
        hash_bytes = self.hashed_password.encode("utf-8")

        return bcrypt.checkpw(pwd_bytes, hash_bytes)