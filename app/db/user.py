from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    nickname: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    # Взаимосвязи с другими таблицами
    ...