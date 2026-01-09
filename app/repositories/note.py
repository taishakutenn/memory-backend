from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.note import Note
from app.db.user import User


class NoteRepository:
    async def get_all_notes_for_current_user(self, db: AsyncSession, current_user_uuid: UUID) -> User:
        # Получаем пользователя и всего его заметки через selectinload
        result = select(User).where(User.uuid == current_user_uuid).options(selectinload(User.notes))
        notes_with_user = (await db.execute(result)).scalar_one()
        return notes_with_user

    async def get_note_by_uuid(self, db: AsyncSession, note_uuid) -> Note | None:
        result = await db.execute(select(Note).where(Note.uuid == note_uuid))
        note = result.scalar_one_or_none()
        return note

    async def create_note(self, db: AsyncSession, note: Note) -> Note:
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    async def delete_note(self, db: AsyncSession, note_uuid: UUID) -> bool:
        stmt = delete(Note).where(Note.uuid == note_uuid).returning(Note.uuid) # returning для проверки на удалённость

        result = await db.execute(stmt)
        await db.commit()

        return result.scalar_one_or_none() is not Note

    async def update_note(self, db: AsyncSession, note: Note) -> Note:
        await db.commit()
        await db.refresh(note)
        return note



