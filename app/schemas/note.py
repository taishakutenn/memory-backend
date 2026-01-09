from uuid import UUID

from app.schemas import TuneModel
from app.schemas.user import UserShow

class ShowNote(TuneModel):
    uuid: UUID
    owner_uuid: UUID
    title: str
    description: str


class ShowNotesWithUser(TuneModel):
    user: UserShow
    notes: list[ShowNote]


class CreateNote(TuneModel):
    title: str
    description: str


class UpdateNote(TuneModel):
    title: str | None = None
    description: str | None = None
