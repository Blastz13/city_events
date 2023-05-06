import json
from typing import List

from pydantic import BaseModel, Field

from app.user.schemas import GetUserListResponseSchema


class AchievementResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    title: str = Field(..., description="title")
    users: List[GetUserListResponseSchema] = Field(..., description="users")
    image_url: str = Field(..., description="image_url")

    class Config:
        orm_mode = True


class Base(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AchievementRequestSchema(Base):
    title: str = Field(..., description="title")

    class Config:
        orm_mode = True


class AssignAchievementRequestSchema(BaseModel):
    user_id: int = Field(..., description="user_id")

    class Config:
        orm_mode = True
