from fastapi import APIRouter

from api.chat.v1.chat import chat_router
from api.comment.v1.comment import comment_router
from api.user.v1.user import user_router as user_v1_router
from api.event.v1.event import event_router as event_v1_router
from api.auth.auth import auth_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(event_v1_router, prefix="/api/v1/events", tags=["Event"])
router.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
router.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
router.include_router(comment_router, prefix="/api/v1/comment", tags=["Comment"])


__all__ = ["router"]
