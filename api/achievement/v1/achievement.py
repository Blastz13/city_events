from typing import List, Optional

from fastapi import APIRouter, Query, UploadFile, File, Depends

from app.achievement.models import Achievement
from app.achievement.schemas import AchievementRequestSchema, AchievementResponseSchema, AssignAchievementRequestSchema
from app.achievement.services import AchievementService
from app.user.schemas import ExceptionResponseSchema
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated
from core.fastapi.dependencies.permission import IsOwnerDependency

achievement_router = APIRouter()


@achievement_router.get(
    "",
    response_model=List[AchievementResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
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
    status_code=200
)
async def get_achievement(achievement_id: int):
    return await AchievementService().get_achievement_or_404(achievement_id)


@achievement_router.post(
    "/",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def create_achievement(achievement: AchievementRequestSchema, file: UploadFile = File(...)):
    return await AchievementService().create_achievement(file, **achievement.dict())


@achievement_router.put(
    "/{id}",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Achievement, "users"))],
    status_code=200
)
async def update_achievement(id: int, achievement: AchievementRequestSchema, file: Optional[UploadFile] = File(None)):
    return await AchievementService().update_achievement(id, file, **achievement.dict())


@achievement_router.delete(
    "/{id}",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Achievement, "users"))],
    status_code=204

)
async def remove_achievement(id: int):
    return await AchievementService().remove_achievement(id)


@achievement_router.post(
    "/{id}",
    response_model=AchievementResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Achievement, "users"))],
    status_code=201
)
async def assign_achievement(id: int, assign: AssignAchievementRequestSchema):
    return await AchievementService().assign_achievement(id, **assign.dict())
