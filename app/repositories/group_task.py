from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.group_task import GroupTask
from app.db.user import User


class GroupTaskRepository:
    async def get_all_group_tasks_for_user(self, db: AsyncSession, owner_uuid: UUID) -> User:
        query = select(User).where(User.uuid == owner_uuid).options(selectinload(User.group_tasks))
        group_tasks_with_user = (await db.execute(query)).scalar_one()
        return group_tasks_with_user

    async def get_group_task_by_title(self, db: AsyncSession, owner_uuid: UUID, title: str) -> GroupTask | None:
        query = select(GroupTask).where(GroupTask.title == title, GroupTask.owner_uuid == owner_uuid)
        result = await db.execute(query)
        group_task = result.scalar_one_or_none()
        return group_task

    async def create_group_task(self, db: AsyncSession, group_task: GroupTask) -> GroupTask:
        db.add(group_task)
        await db.commit()
        await db.refresh(group_task)
        return group_task

    async def delete_group_task(self, db: AsyncSession, owner_uuid: UUID, title: str) -> bool:
        stmt = (
            delete(GroupTask)
            .where(GroupTask.title == title, GroupTask.owner_uuid == owner_uuid)
            .returning(GroupTask.title)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none() is not None

    async def update_group_task(self, db: AsyncSession, group_task: GroupTask) -> GroupTask:
        await db.commit()
        await db.refresh(group_task)
        return group_task
