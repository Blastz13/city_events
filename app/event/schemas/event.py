import datetime
from typing import List

from pydantic import BaseModel, Field
from app.user.schemas import CreateUserResponseSchema


class GetEventResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    rating: int = Field(..., description="Rating")
    date_start: datetime.datetime = Field(..., description="date_start")

    class Config:
        orm_mode = True


class CreateEventRequestSchema(BaseModel):
    title: str = Field(..., description="title")
    description: str = Field(..., description="description")
    link: str = Field(..., description="link")
    date_start: datetime.datetime = Field(..., description="date_start")
    limit_member: int = Field(..., description="limit_member")
    location: str = Field(..., description="location")
    longitude: float = Field(..., description="longitude")
    latitude: float = Field(..., description="latitude")


class CreateEventResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    rating: int = Field(..., description="Rating")
    organizators: List[CreateUserResponseSchema]
    members: List[CreateUserResponseSchema]
    location: str = Field(..., description="location")

    class Config:
        orm_mode = True


class ResponseEventSubscribeSchema(BaseModel):
    user_id: int = Field(..., description="user_id")
    event_id: int = Field(..., description="event_id")

    class Config:
        orm_mode = True
