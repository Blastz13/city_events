from typing import List, Dict

from pydantic import BaseModel, Field, validator, root_validator
from sqlalchemy import select, func

from app.user.models import User, UserRating
from core.db.session import sync_session


class CreateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="Nickname")


class UpdateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    username: str = Field(..., description="Nickname")


class AchievementRequestSchema(BaseModel):
    title: str = Field(..., description="title")

    class Config:
        orm_mode = True


class UserListResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class UserResponseSchema(UserListResponseSchema):
    rating: int = Field(..., description="Rating")
    achievements: List[AchievementRequestSchema]

    @root_validator
    def compute_rating(cls, values) -> Dict:
        result = sync_session.execute(
            select(User.id, func.sum(UserRating.rating))
            .where(User.id == values["id"])
            .join(UserRating, UserRating.evaluated_id == User.id).group_by(User.id))
        result = result.unique().first()
        if result:
            values["rating"] = result[1]
        else:
            values["rating"] = 0
        return values

    class Config:
        orm_mode = True


class RateUserRequestSchema(BaseModel):
    evaluated_id: int = Field(..., description="evaluated_id")
    rating: int = Field(..., description="rating")

    @validator('rating')
    def limit_rating(cls, value):
        if value > 10:
            raise ValueError('The rating value should be no more than 10')
        return value

    class Config:
        orm_mode = True


class RateUserResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    evaluated_id: int = Field(..., description="evaluated_id")
    user_id: int = Field(..., description="evaluated_id")
    rating: int = Field(..., description="rating")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
