from uuid import UUID

from app.schemas import TuneModel
from app.schemas.user import UserShow

class ShowNote(TuneModel):
    owner_uuid: UUID
    title: str
    description: str


class ShowNotesWithUser(TuneModel):
    user: UserShow
    notes: list[ShowNote]

