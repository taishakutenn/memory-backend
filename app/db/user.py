from app.db.base import Base
from app.db.note import Note
from app.db.task import Task
from app.db.group_task import GroupTask

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from uuid import UUID, uuid4


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    nickname: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    # Взаимосвязи с другими таблицами
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="owner") # Заметки
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")  # Задачи
    group_tasks: Mapped[list["GroupTask"]] = relationship("GroupTask", back_populates="owner") # Группы задач