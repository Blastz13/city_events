from typing import List, Dict

from sqlalchemy import select, update

from app.achievement.models import Achievement
from app.user.models import User
from core.db import session


class AchievementService:
    def __init__(self):
        ...

    @classmethod
    async def get_achievement_list(
            cls,
            limit: int = 12,
    ) -> List[Achievement]:
        query = select(Achievement)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_achievement(cls, id: int) -> Achievement:
        achievement = await session.scalar(
            select(Achievement).where(Achievement.id == id))
        return achievement

    @classmethod
    async def create_achievement(cls, **kwargs) -> Achievement:
        achievement = Achievement(**kwargs)
        session.add(achievement)
        await session.commit()
        await session.refresh(achievement)
        return achievement

    async def update_achievement(
            self,
            id: int,
            **kwargs: dict,
    ) -> Achievement:
        query = (
            update(Achievement)
            .where(Achievement.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(query)
        await session.commit()
        return await self.get_achievement(id)

    @classmethod
    async def remove_achievement(cls, id: int) -> Dict:
        achievement = await session.scalar(select(Achievement).where(Achievement.id == id))
        await session.delete(achievement)
        await session.commit()
        return {}

    async def assign_achievement(self, achievement_id: int, user_id) -> Achievement:
        achievement = await self.get_achievement(achievement_id)
        user = await session.scalar(select(User).where(User.id == user_id))
        achievement.users.append(user)
        session.add(achievement)
        await session.commit()
        await session.refresh(achievement)
        return achievement
