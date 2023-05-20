import os
from typing import List, Dict

from fastapi import UploadFile
from sqlalchemy import select, update

from app.achievement.models import Achievement
from app.user.services import UserService
from core.config import config
from core.db import session
from core.exceptions import NotFoundException
from core.fastapi.dependencies.permission import is_privileged_or_admin


class AchievementService:
    def __init__(self):
        ...

    @classmethod
    async def get_achievement_list(
            cls,
            limit: int = 10,
    ) -> List[Achievement]:
        query = select(Achievement).limit(limit)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_achievement_or_404(cls, id: int) -> Achievement:
        result = await session.execute(
            select(Achievement).where(Achievement.id == id))
        instance = result.scalar()
        if not instance:
            raise NotFoundException
        return instance

    @classmethod
    @is_privileged_or_admin
    async def create_achievement(cls, file: UploadFile, user_id, **kwargs: dict) -> Achievement:
        path = f"{os.path.join(config.MEDIA_URL, file.filename)}"
        with open(path, "wb") as buffer:
            buffer.write(await file.read())
        achievement = Achievement(image_url=path, **kwargs)
        session.add(achievement)
        await session.commit()
        await session.refresh(achievement)
        return achievement

    @is_privileged_or_admin
    async def update_achievement(
            self,
            id: int,
            file: UploadFile,
            **kwargs: dict,
    ) -> Achievement:
        if file:
            path = f"{os.path.join(config.MEDIA_URL, file.filename)}"
            with open(path, "wb") as buffer:
                buffer.write(await file.read())
            kwargs["image_url"] = path

        query = (
            update(Achievement)
            .where(Achievement.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(query)
        await session.commit()
        return await self.get_achievement_or_404(id)

    @is_privileged_or_admin
    async def remove_achievement(self, id: int, **kwargs) -> Dict:
        achievement = await self.get_achievement_or_404(id)
        await session.delete(achievement)
        await session.commit()
        return {}

    async def assign_achievement(self, achievement_id: int, user_id: int) -> Achievement:
        achievement = await self.get_achievement_or_404(achievement_id)
        user = await UserService().get_user_or_404(user_id)
        achievement.users.append(user)
        session.add(achievement)
        await session.commit()
        await session.refresh(achievement)
        return achievement
