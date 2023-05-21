import datetime
from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.requests import Request

from app.event.models import Event
from app.event.schemas import (
    EventListResponseSchema,
    CreateEventRequestSchema,
    EventResponseSchema,
    ExceptionResponseSchema,
    EventSubscribeResponseSchema,
    UpdateEventRequestSchema,
)
from app.event.services import EventService
from core.fastapi.dependencies.permission import IsOwnerDependency, PermissionDependency, IsAuthenticated
from core.helpers.cache import Cache, CacheTag

event_router = APIRouter()


@event_router.get(
    "",
    response_model=List[EventListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
@Cache.cached(tag=CacheTag.GET_EVENT_LIST, ttl=60)
async def get_event_list(
        skip: int = Query(default=None, description="Offset"),
        limit: int = Query(default=None, description="Limit"),
):
    return await EventService().get_event_list(skip=skip, limit=limit)


@event_router.get(
    "/search",
    response_model=List[EventListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
@Cache.cached(tag=CacheTag.GET_EVENTS_BY_QUERY, ttl=60)
async def get_events_by_query(query: str = Query(None),
                              date_start: datetime.date = Query(None),
                              date_end: datetime.date = Query(None),
                              offset: int = Query(None),
                              limit: int = Query(None)):
    return await EventService().get_events_by_query(query, date_start, date_end, offset, limit)


@event_router.get(
    "/upcoming",
    response_model=List[EventListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
async def get_upcoming_events():
    return await EventService().get_upcoming_events()


@event_router.get(
    "/radius",
    response_model=List[EventListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
@Cache.cached(tag=CacheTag.GET_EVENTS_BY_RADIUS, ttl=60)
async def get_events_by_radius(
        longitude: float = Query(None, description="longitude"),
        latitude: float = Query(None, description="latitude"),
        radius: int = Query(1000, description="radius")
):
    return await EventService().get_events_by_radius(radius, longitude=longitude, latitude=latitude)


@event_router.get(
    "/{event_id}",
    response_model=EventResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
async def get_event(event_id: int):
    return await EventService().get_event_or_404(event_id)


@event_router.post(
    "",
    response_model=EventResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def create_event(request: Request, event: CreateEventRequestSchema):
    return await EventService().create_event(**event.dict(), user_id=request.user.id)


@event_router.post(
    "/{event_id}/invite",
    response_model=EventResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def add_member_to_event(event_id: int, request: Request):
    return await EventService().add_members_to_event(user_id=request.user.id, event_id=event_id)


@event_router.get(
    "/{event_id}/subscribers",
    response_model=List[EventSubscribeResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
async def get_event_subscribers(event_id: int):
    return await EventService().get_event_subscribers(event_id=event_id)


@event_router.post(
    "/{event_id}/subscribe",
    response_model=EventSubscribeResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def subscribe_to_event(event_id: int, request: Request):
    return await EventService().subscribe_to_event(user_id=request.user.id, event_id=event_id)


@event_router.delete(
    "/{event_id}/unsubscribe",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=204
)
async def unsubscribe_from_event(event_id: int, request: Request):
    return await EventService().unsubscribe_from_event(user_id=request.user.id, event_id=event_id)


@event_router.put(
    "/{id}",
    response_model=EventResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Event, "organizators"))],
    status_code=200
)
async def update_event(id: int, event: UpdateEventRequestSchema):
    return await EventService().update_by_id(id, **event.dict(exclude_unset=True))


@event_router.delete(
    "/{id}",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Event, "organizators"))],
    status_code=204
)
async def remove_event(id: int):
    return await EventService().remove_event(id)
