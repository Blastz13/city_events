import json

from pydantic import BaseModel, Field

from app.event.schemas import GetEventResponseSchema
from app.user.schemas import CreateUserResponseSchema


class Base(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CommentResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    rating: int = Field(..., description="rating")
    comment: str = Field(..., description="comment")
    user: CreateUserResponseSchema = Field(..., description="user")
    event: GetEventResponseSchema = Field(..., description="event")
    likes: int = Field(..., description="likes")
    image_url: str | None = Field(..., description="image_url")

    class Config:
        orm_mode = True


class CommentRequestSchema(Base):
    comment: str = Field(..., description="comment")

    class Config:
        orm_mode = True
