from typing import List, Dict

import requests
import logging
from sqlalchemy import select, update, func, DateTime, or_
import datetime

from app.user.services import UserService
from core.config import config
from core.db import session
from app.event.models import Event, EventSubscribers
from core.db.elastic_db import es_client
from core.exceptions import NotFoundException, BadRequestException, ForbiddenException

logger = logging.getLogger("app")


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
    async def get_events_by_query(cls, query: str, date_start: datetime.date,
                                  date_end: datetime.date, offset: int, limit: int) -> List[Event]:
        elastic_query = {
            "query": {
                "bool": {

                },
            },
            "sort": [
                {"date_start": {"order": "desc"}}
            ],
            "from": offset,
            "size": limit
        }
        if (date_start or date_end) and query:
            elastic_query["query"]["bool"]["must"] = [
                {
                    "range": {
                        "date_start": {
                            "gte": date_start,
                            "lte": date_end,
                            "format": "yyyy-MM-dd",
                        }
                    }
                },
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "description"],
                        "fuzziness": "AUTO",
                        "fuzzy_transpositions": True,
                        "type": "best_fields",
                        "operator": "or"
                    }
                }
            ]
        else:
            elastic_query["query"]["bool"]["should"] = [
                {
                    "range": {
                        "date_start": {
                            "format": "yyyy-MM-dd",
                        }
                    }
                },
            ]

            if date_start:
                elastic_query["query"]["bool"]["should"][0]["range"]["date_start"]["gte"] = date_start
            if date_end:
                elastic_query["query"]["bool"]["should"][0]["range"]["date_start"]["lte"] = date_end
            if query:
                elastic_query["query"]["bool"]["should"].append({
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "description"],
                        "fuzziness": "AUTO",
                        "fuzzy_transpositions": True,
                        "type": "best_fields",
                        "operator": "or"
                    }
                })

        results = await es_client.search(index=config.ELASTICSEARCH_INDEX, body=elastic_query)
        event_ids = [int(result["_id"]) for result in results["hits"]["hits"]]
        events = await session.scalars(select(Event).where(Event.id.in_(event_ids)))
        return events.unique().all()

    @classmethod
    async def get_event_or_404(cls, id: int) -> Event:
        result = await session.execute(select(Event).where(Event.id == id))
        instance = result.scalar()
        if not instance:
            raise NotFoundException
        return instance

    @classmethod
    async def create_event(cls, **kwargs) -> Event:
        kwargs["geo"] = 'POINT({} {})'.format(kwargs["longitude"], kwargs["latitude"])
        user_id = kwargs.pop("user_id")
        user = await UserService().get_user_or_404(user_id)
        if await UserService().get_user_rating(user.id) >= 1000 or await UserService().is_admin(user.id):
            event = Event(**kwargs)
            event.organizators.append(user)
            event.members.append(user)
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event
        else:
            raise ForbiddenException

    async def add_members_to_event(self, user_id: int, event_id: int) -> Event:
        event = await self.get_event_or_404(event_id)
        if len(event.members) < event.limit_member:
            user = await UserService().get_user_or_404(user_id)
            event.members.append(user)
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event
        raise BadRequestException

    async def subscribe_to_event(self, user_id: int, event_id: int) -> Event:
        event = await self.get_event_or_404(event_id)
        user = await UserService().get_user_or_404(user_id)
        event_subscribe = EventSubscribers(user_id=user.id, event_id=event.id)
        session.add(event_subscribe)
        await session.commit()
        await session.refresh(event_subscribe)
        return event_subscribe

    async def unsubscribe_from_event(self, user_id: int, event_id: int) -> Dict:
        event = await self.get_event_or_404(event_id)
        user = await UserService().get_user_or_404(user_id)
        event_subscribe = await session.scalar(select(EventSubscribers).where(EventSubscribers.user_id == user.id,
                                                                              EventSubscribers.event_id == event.id))
        if event_subscribe:
            await session.delete(event_subscribe)
            await session.commit()
        return {}

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
        return await self.get_event_or_404(id)

    async def remove_event(self, id: int) -> Dict:
        event = await self.get_event_or_404(id)
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
            select(Event).where(or_(func.coalesce(Event.date_start).cast(DateTime) > datetime.datetime.now(),
                                    func.coalesce(Event.date_start).cast(DateTime) <= datetime.datetime.now()
                                    + datetime.timedelta(minutes=30))).order_by(Event.date_start))
        return events.unique().all()

    @classmethod
    def get_address_by_latitude_longitude(cls, lat, lng):
        try:
            url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lng}&format=json'
            response = requests.get(url).json()
            if 'address' in response.keys():
                address = response['address']
                return f"{address['city']} {address['road']} {address['house_number']}"
            else:
                return None
        except Exception as ex:
            logger.error(ex)
            return None

    @classmethod
    def get_latitude_longitude_by_address(cls, address):
        try:
            url = f'https://nominatim.openstreetmap.org/search.php?q={address}&format=json'
            response = requests.get(url).json()
            if len(response) > 0:
                lat = response[0]['lat']
                lon = response[0]['lon']
                return lat, lon
            else:
                return None
        except Exception as ex:
            logger.error(ex)
            return None
