from typing import List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File
from starlette.requests import Request

from app.comment.schemas import CommentRequestSchema, CommentResponseSchema
from app.comment.services import CommentService
from app.user.schemas import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsOwnerDependency, PermissionDependency, IsAuthenticated

comment_router = APIRouter()


@comment_router.get(
    "/event/{event_id}",
    response_model=List[CommentResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_comment_list(
        event_id: int,
        limit: int = Query(10, description="Limit"),
):
    return await CommentService().get_comment_list_by_event(event_id=event_id, limit=limit)


@comment_router.get(
    "/{comment_id}",
    response_model=CommentResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_comment(comment_id: int):
    return await CommentService().get_comment(comment_id)


@comment_router.post(
    "/{event_id}",
    response_model=CommentResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def create_comment(request: Request, event_id: int, comment: CommentRequestSchema,
                         file: Optional[UploadFile] = File(None)):
    return await CommentService().create_comment(file, **comment.dict(), user_id=request.user.id, event_id=event_id)


@comment_router.put(
    "/{comment_id}",
    response_model=CommentResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=201,
    # dependencies=[Depends(IsOwnerDependency(Comment))],
)
async def update_comment(comment_id: int, comment: CommentRequestSchema, file: Optional[UploadFile] = File(None)):
    return await CommentService().update_comment(comment_id, file, **comment.dict())


@comment_router.delete(
    "/{comment_id}",
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=204,
    # dependencies=[Depends(IsOwnerDependency())],
)
async def remove_comment(comment_id: int):
    return await CommentService().remove_comment(comment_id)
