import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel, Field, root_validator

from app.comment.schemas import CommentResponseSchema
from app.user.schemas import UserListResponseSchema


class CreateEventRequestSchema(BaseModel):
    title: str = Field(..., description="title")
    description: str = Field(..., description="description")
    link: str = Field(..., description="link")
    date_start: datetime.datetime = Field(..., description="date_start")
    limit_member: int = Field(..., description="limit_member")
    location: str = Field(..., description="location")
    longitude: float = Field(..., description="longitude")
    latitude: float = Field(..., description="latitude")


class UpdateEventRequestSchema(BaseModel):
    title: Optional[str] = Field(None, description="title")
    description: Optional[str] = Field(None, description="description")
    link: Optional[str] = Field(None, description="link")
    date_start: Optional[datetime.datetime] = Field(None, description="date_start")
    limit_member: Optional[int] = Field(None, description="limit_member")
    location: Optional[str] = Field(None, description="location")
    longitude: Optional[float] = Field(None, description="longitude")
    latitude: Optional[float] = Field(None, description="latitude")


class EventListResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    rating: int = Field(..., description="Rating")
    date_start: datetime.datetime = Field(..., description="date_start")
    location: str = Field(..., description="location")
    comments: List[CommentResponseSchema] = Field(exclude=True)

    @root_validator
    def compute_rating(cls, values) -> Dict:
        values["rating"] = sum([
            comment.rating
            for comment in values["comments"]
        ])
        return values

    class Config:
        orm_mode = True


class EventResponseSchema(EventListResponseSchema):
    organizators: List[UserListResponseSchema]
    members: List[UserListResponseSchema]
    comments: List[CommentResponseSchema]

    class Config:
        orm_mode = True


class EventSubscribeResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    user_id: int = Field(..., description="user_id")
    event_id: int = Field(..., description="event_id")

    class Config:
        orm_mode = True
