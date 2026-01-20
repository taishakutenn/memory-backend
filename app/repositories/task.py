from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.task import Task
from app.db.user import User


class TaskRepository:
    async def get_all_tasks_for_user(self, db: AsyncSession, owner_uuid: UUID) -> User:
        query = select(User).where(User.uuid == owner_uuid).options(selectinload(User.tasks))
        tasks_with_user = (await db.execute(query)).scalar_one()
        return tasks_with_user

    async def create_task(self, db: AsyncSession, task: Task) -> Task:
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

