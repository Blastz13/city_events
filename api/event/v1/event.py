from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.requests import Request

from app.event.models import Event
from app.event.schemas import (
    GetEventListResponseSchema,
    CreateEventRequestSchema,
    CreateEventResponseSchema,
)
from app.event.services import EventService
from core.fastapi.dependencies.permission import IsOwnerDependency

event_router = APIRouter()


@event_router.get(
    "",
    response_model=List[GetEventListResponseSchema],
    # responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_event_list(
        limit: int = Query(10, description="Limit"),
):
    return await EventService().get_event_list(limit=limit)


@event_router.get(
    "/{event_id}",
    response_model=CreateEventResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_event(event_id: int):
    return await EventService().get_event(event_id)


@event_router.post(
    "",
    response_model=CreateEventResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def create_event(request: Request, event: CreateEventRequestSchema):
    return await EventService().create_event(**event.dict(), user_id=request.user.id)


@event_router.post(
    "/{event_id}/invite",
    response_model=CreateEventResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def add_member_to_event(event_id: int, request: Request):
    return await EventService().add_members_to_event(user_id=request.user.id, event_id=event_id)


@event_router.put(
    "/{event_id}",
    response_model=CreateEventResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
    status_code=201,
    dependencies=[Depends(IsOwnerDependency(Event))],
)
async def update_event(event_id: int, event: CreateEventRequestSchema):
    return await EventService().update_by_id(event_id, **event.dict())


@event_router.delete(
    "/{event_id}",
    # response_model=CreateEventResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
    status_code=204,
    dependencies=[Depends(IsOwnerDependency(Event))],
)
async def remove_event(event_id: int):
    return await EventService().remove_event(event_id)
