from typing import List

from pydantic import BaseModel, Field


class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="Nickname")
    rating: int = Field(..., description="Rating")

    class Config:
        orm_mode = True


class CreateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="Nickname")


class UpdateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    username: str = Field(..., description="Nickname")


class CreateUserResponseSchema(BaseModel):
    email: str = Field(..., description="Email")
    username: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class AchievementRequestSchema(BaseModel):
    title: str = Field(..., description="title")

    class Config:
        orm_mode = True


class GetUserResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="Nickname")
    rating: int = Field(..., description="Rating")
    achievements: List[AchievementRequestSchema]

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
