from app.db.base import Base
# from app.db.user import User
# from app.db.group_task import GroupTask

from datetime import datetime

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMP

from uuid import UUID, uuid4

class Task(Base):
    __tablename__ = "tasks"

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    group_title: Mapped[str] = mapped_column(String, ForeignKey("group_tasks.title"), nullable=True) # Группа задач
    title: Mapped[str] = mapped_column(String(100), unique=False, index=True, nullable=True)
    date_start_period: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0))
    date_end_period: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0))
    status: Mapped[str] = mapped_column(String(20), default="В процессе")

    # Взаимосвязи с другими таблицами
    owner: Mapped["User"] = relationship("User", back_populates="tasks")
    group: Mapped["GroupTask"] = relationship("GroupTask", back_populates="tasks")