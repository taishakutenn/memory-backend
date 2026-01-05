from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.user import UserNotFound
from app.repositories.note import NoteRepository
from app.repositories.user import UserRepository
from app.db.note import Note
from app.db.user import User


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()
        self.user_repo = UserRepository()

    async def get_all_notes_for_current_user(self, db: AsyncSession, current_user_uuid: UUID) -> dict:
        notes_with_user = await self.note_repo.get_all_notes_for_current_user(db, current_user_uuid)
        result = {
            "user": notes_with_user,
            "notes": notes_with_user.notes
        }

        return result

    async def create_note(self, db: AsyncSession, owner_uuid: UUID, title: str, description: str) -> Note | None:
        # Проверяем, существует ли пользователь
        user = self.user_repo.get_user_by_uuid(db, owner_uuid)
        if user is None:
            raise UserNotFound()

        note = await self.note_repo.create_note(db, owner_uuid, title, description)
        return note
