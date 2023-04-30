from typing import List

from fastapi import APIRouter, Query

from app.achievement.schemas import AchievementRequestSchema, AchievementResponseSchema, AssignAchievementRequestSchema
from app.achievement.services import AchievementService
from app.user.schemas import ExceptionResponseSchema

achievement_router = APIRouter()


@achievement_router.get(
    "",
    response_model=List[AchievementResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
    status_code=200
)
async def get_achievement_list(
        limit: int = Query(10, description="Limit"),
):
    return await AchievementService().get_achievement_list(limit=limit)


@achievement_router.get(
    "/{achievement_id}",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=200
)
async def get_achievement(achievement_id: int):
    return await AchievementService().get_achievement(achievement_id)


@achievement_router.post(
    "/",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def create_achievement(achievement: AchievementRequestSchema):
    return await AchievementService().create_achievement(**achievement.dict())


@achievement_router.put(
    "/{achievement_id}",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200,
    # dependencies=[Depends(IsOwnerDependency(Comment))],
)
async def update_achievement(achievement_id: int, achievement: AchievementRequestSchema):
    return await AchievementService().update_achievement(achievement_id, **achievement.dict())


@achievement_router.delete(
    "/{achievement_id}",
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=204,
    # dependencies=[Depends(IsOwnerDependency())],
)
async def remove_achievement(achievement_id: int):
    return await AchievementService().remove_achievement(achievement_id)


@achievement_router.post(
    "/{achievement_id}",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=201,
    # dependencies=[Depends(IsOwnerDependency())],
)
async def assign_achievement(achievement_id: int, assign: AssignAchievementRequestSchema):
    return await AchievementService().assign_achievement(achievement_id, **assign.dict())
