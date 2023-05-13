import os
from typing import List, Dict

from fastapi import UploadFile
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.comment.models import Comment
from core.config import config
from core.db import session
from core.exceptions import NotFoundException


class CommentService:
    def __init__(self):
        ...

    @classmethod
    async def get_comment_list_by_event(
            cls,
            event_id: int,
            limit: int = 12,
    ) -> List[Comment]:
        query = select(Comment).options(selectinload(Comment.event)).where(Comment.event_id == event_id)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_comment_or_404(cls, id: int) -> Comment:
        result = await session.execute(select(Comment).options(selectinload(Comment.event)).where(Comment.id == id))
        instance = result.scalar()
        if not instance:
            raise NotFoundException
        return instance

    @classmethod
    async def create_comment(cls, file: UploadFile, **kwargs) -> Comment:
        if file:
            path = f"{os.path.join(config.MEDIA_URL, file.filename)}"
            with open(path, "wb") as buffer:
                buffer.write(await file.read())
            kwargs["image_url"] = path

        comment = Comment(**kwargs)
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    async def update_comment(
            self,
            id: int,
            file: UploadFile,
            **kwargs: dict,
    ) -> Comment:

        if file:
            path = f"{os.path.join(config.MEDIA_URL, file.filename)}"
            with open(path, "wb") as buffer:
                buffer.write(await file.read())
            kwargs["image_url"] = path

        query = (
            update(Comment)
            .where(Comment.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(query)
        await session.commit()
        return await self.get_comment_or_404(id)

    async def remove_comment(self, id: int) -> Dict:
        comment = await self.get_comment_or_404(id)
        await session.delete(comment)
        await session.commit()
        return {}
