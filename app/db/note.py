from app.db.base import Base
# from app.db.user import User

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from uuid import UUID, uuid4

class Note(Base):
    __tablename__ = "notes"

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), unique=False, index=True, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Взаимосвязи с другими таблицами
    owner: Mapped["User"] = relationship("User", back_populates="notes")