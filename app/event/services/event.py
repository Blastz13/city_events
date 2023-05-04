from typing import List, Dict

from sqlalchemy import select, update, func, DateTime
import datetime

from app.user.models import User
from app.user.services import UserService
from core.db import session
from app.event.models import Event
from core.db.elastic_db import es_client, ELASTICSEARCH_INDEX


class EventService:
    def __init__(self):
        ...

    @classmethod
    async def get_event_list(
            cls,
            skip: int,
            limit: int,
    ) -> List[Event]:
        result = await session.execute(select(Event).offset(skip).limit(limit).order_by(Event.id))
        return result.scalars().unique().all()

    @classmethod
    async def get_events_by_query(cls, query: str) -> List[Event]:
        if query:
            results = await es_client.search(index=ELASTICSEARCH_INDEX, body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "description"],
                        "fuzziness": "AUTO",
                        "fuzzy_transpositions": True,
                        "type": "best_fields",
                        "operator": "or"
                    }
                },
                "sort": [
                    {"date_start": {"order": "desc"}}
                ]
            })
            event_ids = [int(result["_id"]) for result in results["hits"]["hits"]]
            events = await session.scalars(select(Event).where(Event.id.in_(event_ids)))
        else:
            events = await session.scalars(select(Event))
        return events.unique().all()

    @classmethod
    async def get_event(cls, id: int) -> Event:
        return await session.scalar(select(Event).where(Event.id == id))

    @classmethod
    async def create_event(cls, **kwargs) -> Event:
        kwargs["geo"] = 'POINT({} {})'.format(kwargs["longitude"], kwargs["latitude"])
        user_id = kwargs.pop("user_id")
        user = await UserService().get_user(user_id)
        event = Event(**kwargs)
        event.organizators.append(user)
        event.members.append(user)
        session.add(event)
        await session.commit()
        await session.refresh(event)
        return event

    async def add_members_to_event(self, user_id: int, event_id: int) -> Event:
        event = await self.get_event(event_id)
        user = await UserService().get_user(user_id)
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

    async def remove_event(self, id: int) -> Dict:
        event = await self.get_event(id)
        await session.delete(event)
        await session.commit()
        return {}

    @classmethod
    async def get_events_by_radius(cls, radius: int, longitude: float, latitude: float) -> List[Event]:
        data = await session.scalars(select(Event)
                                     .where(func.ST_DistanceSphere(Event.geo,
                                                                   func.ST_GeomFromText(
                                                                       f"POINT({longitude} {latitude})")) < radius,
                                            func.coalesce(Event.date_start).cast(
                                                DateTime) >= datetime.datetime.now() - datetime.timedelta(minutes=60)))
        return data.unique().all()

    @classmethod
    async def get_upcoming_events(cls) -> List[Event]:
        events = await session.scalars(
            select(Event).where(func.coalesce(Event.date_start).cast(DateTime) > datetime.datetime.now(),
                                func.coalesce(Event.date_start).cast(DateTime) <= datetime.datetime.now()
                                + datetime.timedelta(minutes=30)).order_by(Event.date_start))
        return events.unique().all()
