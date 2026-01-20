from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task import TaskRepository
from app.db.task import Task
from app.schemas.task import CreateTask


class TaskService:
    def __init__(self):
        self.task_repo = TaskRepository()

    async def get_all_tasks_for_current_user(self, db: AsyncSession, owner_uuid: UUID) -> dict:
        tasks_with_user = await self.task_repo.get_all_tasks_for_user(db, owner_uuid)
        return {
            "user": tasks_with_user,
            "tasks": tasks_with_user.tasks
        }

    async def create_task(self, db: AsyncSession, owner_uuid: UUID, data: CreateTask) -> Task:
        task = Task(
            owner_uuid=owner_uuid,
            group_title=data.group_title,
            title=data.title,
            date_start_period=data.date_start_period,
            date_end_period=data.date_end_period,
            status=data.status,
        )
        return await self.task_repo.create_task(db, task)

