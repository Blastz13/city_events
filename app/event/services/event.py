from typing import List, Dict

from sqlalchemy import select, update, func

from app.user.models import User
from core.db import session
from app.event.models import Event


class EventService:
    def __init__(self):
        ...

    @classmethod
    async def get_event_list(
            cls,
            limit: int = 12,
    ) -> List[User]:
        query = select(Event)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_event(cls, id: int) -> Event:
        return await session.scalar(select(Event).where(Event.id == id))

    @classmethod
    async def create_event(cls, **kwargs):
        kwargs["geo"] = 'POINT({} {})'.format(kwargs["longitude"], kwargs["latitude"])
        user_id = kwargs.pop("user_id")
        event = Event(**kwargs)
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().all()
        event.organizators = user
        event.members = user
        session.add(event)
        await session.commit()
        await session.refresh(event)
        return event

    @classmethod
    async def add_members_to_event(cls, user_id: int, event_id: int) -> Event:
        event = await session.scalar(select(Event).where(Event.id == event_id))
        user = await session.scalar(select(User).where(User.id == user_id))
        event.members.append(user)
        session.add(event)
        await session.commit()
        await session.refresh(event)
        return event

    async def update_by_id(
            self,
            id: int,
            **kwargs: dict,
    ) -> Event:
        query = (
            update(Event)
            .where(Event.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(query)
        await session.commit()
        return await self.get_event(id)

    @classmethod
    async def remove_event(cls, id: int) -> Dict:
        event = await session.scalar(select(Event).where(Event.id == id))
        await session.delete(event)
        await session.commit()
        return {}

    @classmethod
    async def get_events_by_radius(cls, radius: int, longitude: float, latitude: float) -> Dict:
        data = await session.scalars(select(Event)
                                     .where(func.ST_DistanceSphere(Event.geo,
                                            func.ST_GeomFromText(f"POINT({longitude} {latitude})")) < radius))
        return data.unique().all()
