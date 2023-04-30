from typing import List

from pydantic import BaseModel, Field

from app.user.schemas import GetUserListResponseSchema


class AchievementResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    title: str = Field(..., description="title")
    users: List[GetUserListResponseSchema] = Field(..., description="users")

    class Config:
        orm_mode = True


class AchievementRequestSchema(BaseModel):
    title: str = Field(..., description="title")

    class Config:
        orm_mode = True


class AssignAchievementRequestSchema(BaseModel):
    user_id: int = Field(..., description="user_id")

    class Config:
        orm_mode = True
