from fastapi import APIRouter

from app.api.routes.user import user_router
from app.api.routes.auth import auth_router
from app.api.routes.note import note_router

main_router = APIRouter()
main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_router.include_router(note_router, prefix="/note", tags=["note"])
