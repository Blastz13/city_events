from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.requests import Request

from api.user.v1.request.user import LoginRequest
from api.user.v1.response.user import LoginResponse
from app.user.models import UserRating
from app.user.schemas import (
    ExceptionResponseSchema,
    CreateUserRequestSchema,
    UserListResponseSchema,
    UserResponseSchema,
    UpdateUserRequestSchema,
    RateUserRequestSchema,
    RateUserResponseSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
)
from core.fastapi.dependencies.permission import IsOwnerDependency, IsAuthenticated

user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[UserListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
async def get_user_list(
        limit: int = Query(10, description="Limit"),
        prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=UserListResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=201
)
async def create_user(request: CreateUserRequestSchema):
    return await UserService().create_user(**request.dict())


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
    response_model=UserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
)
async def get_user(user_id: int):
    return await UserService().get_user_or_404(user_id=user_id)


@user_router.post(
    "/rate",
    response_model=RateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def rate_user(request: Request, rate: RateUserRequestSchema):
    return await UserService().add_user_rating(user_id=request.user.id, **rate.dict())


@user_router.post(
    "/rate",
    response_model=RateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def add_rate_user(request: Request, rate: RateUserRequestSchema):
    return await UserService().add_user_rating(user_id=request.user.id, **rate.dict())


@user_router.delete(
    "/{id}/rate",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(UserRating, "user_id"))],
    status_code=200
)
async def remove_rate_user(id: int):
    return await UserService().remove_user_rating(id)


@user_router.put(
    "/",
    response_model=UserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=200
)
async def update_user(request: Request, user: UpdateUserRequestSchema):
    return await UserService().update_by_id(request.user.id, **user.dict(exclude_unset=True))
