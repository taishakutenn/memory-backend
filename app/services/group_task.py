from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.group_task import GroupTaskNotFound
from app.security.exceptions import AccessDenied
from app.repositories.group_task import GroupTaskRepository
from app.db.group_task import GroupTask
from app.schemas.group_task import CreateGroupTask, UpdateGroupTask


class GroupTaskService:
    def __init__(self):
        self.group_task_repo = GroupTaskRepository()

    async def _get_group_task_for_user(self, db: AsyncSession, owner_uuid: UUID, title: str) -> GroupTask:
        group_task = await self.group_task_repo.get_group_task_by_title(db, owner_uuid, title)

        if group_task is None:
            raise GroupTaskNotFound()

        if group_task.owner_uuid != owner_uuid:
            raise AccessDenied()

        return group_task

    async def get_all_group_tasks_for_current_user(self, db: AsyncSession, owner_uuid: UUID) -> dict:
        group_tasks_with_user = await self.group_task_repo.get_all_group_tasks_for_user(db, owner_uuid)
        return {
            "user": group_tasks_with_user,
            "group_tasks": group_tasks_with_user.group_tasks
        }

    async def create_group_task(self, db: AsyncSession, owner_uuid: UUID, data: CreateGroupTask) -> GroupTask:
        group_task = GroupTask(
            title=data.title,
            owner_uuid=owner_uuid
        )
        return await self.group_task_repo.create_group_task(db, group_task)

    async def delete_group_task(self, db: AsyncSession, owner_uuid: UUID, title: str) -> bool:
        await self._get_group_task_for_user(db, owner_uuid, title)
        return await self.group_task_repo.delete_group_task(db, owner_uuid, title)

    async def update_group_task(self, db: AsyncSession, owner_uuid: UUID, title: str, data: UpdateGroupTask) -> GroupTask:
        group_task = await self._get_group_task_for_user(db, owner_uuid, title)
        updated_data = data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(group_task, field, value)

        return await self.group_task_repo.update_group_task(db, group_task)
