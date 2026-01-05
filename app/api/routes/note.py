from fastapi import APIRouter, Depends, Body

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.db.user import User
from app.security.deps import get_current_active_user
from app.services.note import NoteService
from app.schemas.note import ShowNote, ShowNotesWithUser

note_router = APIRouter()


@note_router.get("/search/all/me", response_model=ShowNotesWithUser)
async def get_all_notes_for_current_user(db: AsyncSession = Depends(get_db),
                                         current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    notes = await note_service.get_all_notes_for_current_user(db, current_user.uuid)
    return notes


@note_router.post("/create", response_model=ShowNote)
async def create_note(body, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    note_service = NoteService()
    note = await note_service.create_note()
    return note
