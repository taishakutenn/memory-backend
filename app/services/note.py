from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.note import NoteNotFound
from app.security.exceptions import AccessDenied
from app.repositories.note import NoteRepository
from app.repositories.user import UserRepository
from app.db.note import Note
from app.schemas.note import CreateNote, UpdateNote


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()
        self.user_repo = UserRepository()

    async def _get_note_for_user(self, db: AsyncSession, owner_uuid: UUID, note_uuid: UUID) -> Note:
        """Функция для проверки принадлежности заметки конкретному пользователю"""
        note = await self.note_repo.get_note_by_uuid(db, note_uuid)

        if note is None:
            raise NoteNotFound()

        if note.owner_uuid != owner_uuid:
            raise AccessDenied()

        return note

    async def get_all_notes_for_current_user(self, db: AsyncSession, current_user_uuid: UUID) -> dict:
        notes_with_user = await self.note_repo.get_all_notes_for_current_user(db, current_user_uuid)
        result = {
            "user": notes_with_user,
            "notes": notes_with_user.notes
        }

        return result

    async def create_note(self, db: AsyncSession, owner_uuid: UUID, note_data: CreateNote) -> Note | None:
        note = Note(
            owner_uuid=owner_uuid,
            title=note_data.title,
            description=note_data.description
        )

        # Передаём заполненый объект в репозиторий для созраниния в БД
        return await self.note_repo.create_note(db, note)

    async def delete_note(self, db: AsyncSession, owner_uuid: UUID, note_uuid: UUID) -> bool:
        # Проверяем, существует ли заметка и относится ли она к переданному пользовтаелю
        note = await self._get_note_for_user(db, owner_uuid, note_uuid)
        is_note_delete = await self.note_repo.delete_note(db, note_uuid)  # True/False
        return is_note_delete

    async def update_note(self, db: AsyncSession, owner_uuid: UUID, note_uuid: UUID, note_data: UpdateNote) -> Note:
        # Так же возвращает наш объект Note из бд
        note = await self._get_note_for_user(db, owner_uuid, note_uuid)
        # Преобразовывам данные в dict, отбрасывая поля, которые явялются None
        updated_note_data = note_data.model_dump(exclude_unset=True)

        for field, value in updated_note_data.items():
            # Записываем в наш orm объект note новые данные
            setattr(note, field, value)

        # Сохраняем note через репозеторий
        updated_note = await self.note_repo.update_note(db, note)
        return updated_note
