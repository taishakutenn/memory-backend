from uuid import UUID

from fastapi import APIRouter, Depends, Body

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.db.user import User
from app.security.deps import get_current_active_user
from app.services.note import NoteService
from app.schemas.note import ShowNote, ShowNotesWithUser, CreateNote, UpdateNote

note_router = APIRouter()


@note_router.get("/search/all/me", response_model=ShowNotesWithUser)
async def get_all_notes_for_current_user(db: AsyncSession = Depends(get_db),
                                         current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    notes = await note_service.get_all_notes_for_current_user(db, current_user.uuid)
    return notes

@note_router.get("/search/by-uuid/{note_uuid}", response_model=ShowNote)
async def get_note_by_uuid(note_uuid: UUID, db: AsyncSession = Depends(get_db),
                                         current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    note = await note_service._get_note_for_user(db, current_user.uuid, note_uuid)
    return note


@note_router.post("/create", response_model=ShowNote)
async def create_note(body: CreateNote, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    note = await note_service.create_note(db, current_user.uuid, body)
    return note


@note_router.delete("/delete/{note_uuid}")
async def delete_note(note_uuid: UUID, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    deleted_note = await note_service.delete_note(db, current_user.uuid, note_uuid)  # Возвращает True/False
    return deleted_note


@note_router.put("/update/{note_uuid}", response_model=ShowNote)
async def update_note(body: UpdateNote, note_uuid: UUID, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    updated_note = await note_service.update_note(db, current_user.uuid, note_uuid, body)
    return updated_note
