from app.db.base import Base
# from app.db.user import User
# from app.db.task import Task

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from uuid import UUID, uuid4

class GroupTask(Base):
    """
    Группа задач
    Например: На год, Новый год, Институт
    """

    __tablename__ = "group_tasks"

    title: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    owner_uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)

    # Взаимосвязи с другими таблицами
    owner: Mapped["User"] = relationship("User", back_populates="group_tasks")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="group")