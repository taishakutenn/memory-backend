from datetime import datetime
from uuid import UUID

from app.schemas import TuneModel
from app.schemas.user import UserShow


class ShowTask(TuneModel):
    uuid: UUID
    owner_uuid: UUID
    group_title: str | None = None
    title: str
    date_start_period: datetime
    date_end_period: datetime
    status: str


class ShowTasksWithUser(TuneModel):
    user: UserShow
    tasks: list[ShowTask]


class CreateTask(TuneModel):
    group_title: str | None = None
    title: str
    date_start_period: datetime
    date_end_period: datetime
    status: str | None = None

