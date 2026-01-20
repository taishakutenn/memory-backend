from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.db.user import User
from app.security.deps import get_current_active_user
from app.services.group_task import GroupTaskService
from app.schemas.group_task import (
    ShowGroupTask,
    ShowGroupTasksWithUser,
    CreateGroupTask,
    UpdateGroupTask
)


group_task_router = APIRouter()


@group_task_router.get("/search/all/me", response_model=ShowGroupTasksWithUser)
async def get_all_group_tasks_for_current_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    group_task_service = GroupTaskService()
    return await group_task_service.get_all_group_tasks_for_current_user(db, current_user.uuid)


@group_task_router.get("/search/by-title/{group_title}", response_model=ShowGroupTask)
async def get_group_task_by_title(
    group_title: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    group_task_service = GroupTaskService()
    return await group_task_service._get_group_task_for_user(db, current_user.uuid, group_title)


@group_task_router.post("/create", response_model=ShowGroupTask)
async def create_group_task(
    body: CreateGroupTask,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    group_task_service = GroupTaskService()
    return await group_task_service.create_group_task(db, current_user.uuid, body)


@group_task_router.delete("/delete/{group_title}")
async def delete_group_task(
    group_title: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    group_task_service = GroupTaskService()
    return await group_task_service.delete_group_task(db, current_user.uuid, group_title)


@group_task_router.put("/update/{group_title}", response_model=ShowGroupTask)
async def update_group_task(
    body: UpdateGroupTask,
    group_title: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    group_task_service = GroupTaskService()
    return await group_task_service.update_group_task(db, current_user.uuid, group_title, body)
