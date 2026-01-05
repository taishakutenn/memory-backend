from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.note import Note
from app.db.user import User


class NoteRepository:
    async def get_all_notes_for_current_user(self, db: AsyncSession, current_user_uuid: UUID) -> User:
        # Получаем пользователя и всего его заметки через selectinload
        result = select(User).where(User.uuid == current_user_uuid).options(selectinload(User.notes))
        notes_with_user = (await db.execute(result)).scalar_one()
        return notes_with_user

    async def create_note(self, db: AsyncSession, owner_uuid: UUID, title: str, description: str):
        note = Note(owner_uuid=owner_uuid, title=title, description=description)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note