from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.db.user import User
from app.security.deps import get_current_active_user
from app.services.task import TaskService
from app.schemas.task import ShowTask, ShowTasksWithUser, CreateTask


task_router = APIRouter()


@task_router.get("/search/all/me", response_model=ShowTasksWithUser)
async def get_all_tasks_for_current_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService()
    return await task_service.get_all_tasks_for_current_user(db, current_user.uuid)


@task_router.post("/create", response_model=ShowTask)
async def create_task(
    body: CreateTask,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService()
    return await task_service.create_task(db, current_user.uuid, body)

