from pydantic import BaseModel, Field

from app.event.schemas import GetEventResponseSchema
from app.user.schemas import CreateUserResponseSchema


class CommentResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    rating: int = Field(..., description="rating")
    comment: str = Field(..., description="comment")
    user: CreateUserResponseSchema = Field(..., description="user")
    event: GetEventResponseSchema = Field(..., description="event")
    likes: int = Field(..., description="likes")

    class Config:
        orm_mode = True


class CommentRequestSchema(BaseModel):
    comment: str = Field(..., description="comment")

    class Config:
        orm_mode = True
