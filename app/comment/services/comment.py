from typing import List, Dict

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.comment.models import Comment
from core.db import session


class CommentService:
    def __init__(self):
        ...

    @classmethod
    async def get_comment_list(
            cls,
            limit: int = 12,
    ) -> List[Comment]:
        query = select(Comment).options(selectinload(Comment.event))

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_comment(cls, id: int) -> Comment:
        data = await session.scalar(select(Comment).options(selectinload(Comment.event)).where(Comment.id == id))
        return data

    @classmethod
    async def create_comment(cls, **kwargs) -> Comment:
        comment = Comment(**kwargs)
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    async def update_comment(
            self,
            id: int,
            **kwargs: dict,
    ) -> Comment:
        query = (
            update(Comment)
            .where(Comment.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(query)
        await session.commit()
        return await self.get_comment(id)

    @classmethod
    async def remove_comment(cls, id: int) -> Dict:
        event = await session.scalar(select(Comment).where(Comment.id == id))
        await session.delete(event)
        await session.commit()
        return {}
