from typing import List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File
from starlette.requests import Request

from app.comment.models import Comment
from app.comment.schemas import CommentRequestSchema, CommentResponseSchema
from app.comment.services import CommentService
from app.user.schemas import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsOwnerDependency, PermissionDependency, IsAuthenticated

comment_router = APIRouter()


@comment_router.get(
    "/event/{event_id}",
    response_model=List[CommentResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=200
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
    status_code=200
)
async def get_comment(comment_id: int):
    return await CommentService().get_comment_or_404(comment_id)


@comment_router.post(
    "/{event_id}",
    response_model=CommentResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=201
)
async def create_comment(request: Request, event_id: int, comment: CommentRequestSchema,
                         file: Optional[UploadFile] = File(None)):
    return await CommentService().create_comment(file, **comment.dict(), user_id=request.user.id, event_id=event_id)


@comment_router.put(
    "/{comment_id}",
    response_model=CommentResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Comment, "user_id"))],
    status_code=200
)
async def update_comment(id: int, comment: CommentRequestSchema, file: Optional[UploadFile] = File(None)):
    return await CommentService().update_comment(id, file, **comment.dict())


@comment_router.delete(
    "/{comment_id}",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(IsOwnerDependency(Comment, "user_id"))],
    status_code=204
)
async def remove_comment(id: int):
    return await CommentService().remove_comment(id)
