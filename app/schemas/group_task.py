from uuid import UUID

from app.schemas import TuneModel
from app.schemas.user import UserShow


class ShowGroupTask(TuneModel):
    title: str
    owner_uuid: UUID


class ShowGroupTasksWithUser(TuneModel):
    user: UserShow
    group_tasks: list[ShowGroupTask]


class CreateGroupTask(TuneModel):
    title: str


class UpdateGroupTask(TuneModel):
    title: str | None = None
