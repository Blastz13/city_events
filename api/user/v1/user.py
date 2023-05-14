from typing import List

from fastapi import APIRouter, Depends, Query

from api.user.v1.request.user import LoginRequest
from api.user.v1.response.user import LoginResponse
from app.user.models import User
from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema, GetUserResponseSchema, UpdateUserRequestSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)
from core.fastapi.dependencies.permission import IsOwnerDependency

user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
    status_code=200
)
async def get_user_list(
        limit: int = Query(10, description="Limit"),
        prev: int = Query(None, description="Prev ID"),
):
    data = await UserService().get_user_list(limit=limit, prev=prev)
    return data


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=201
)
async def create_user(request: CreateUserRequestSchema):
    await UserService().create_user(**request.dict())
    return {"email": request.email, "username": request.username}


@user_router.post(
    "/login",
    response_model=LoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    status_code=201
)
async def login(request: LoginRequest):
    token = await UserService().login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}


@user_router.get(
    "/{user_id}",
    response_model=GetUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
async def get_user(user_id: int):
    return await UserService().get_user_or_404(user_id=user_id)


@user_router.put(
    "/{id}",
    response_model=GetUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(User, "id"))],
    status_code=200
)
async def update_user(id: int, user: UpdateUserRequestSchema):
    return await UserService().update_by_id(id, **user.dict())
