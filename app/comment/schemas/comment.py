import json
from typing import Optional

from pydantic import BaseModel, Field

from app.user.schemas import UserListResponseSchema


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
    user: UserListResponseSchema = Field(..., description="user")
    likes: int = Field(..., description="likes")
    image_url: str | None = Field(..., description="image_url")

    class Config:
        orm_mode = True


class CreateCommentRequestSchema(Base):
    comment: str = Field(..., description="comment")
    rating: int = Field(..., description="rating")

    class Config:
        orm_mode = True


class UpdateCommentRequestSchema(Base):
    comment: Optional[str] = Field(None, description="comment")
    rating: Optional[int] = Field(None, description="rating")

    class Config:
        orm_mode = True
