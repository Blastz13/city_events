from fastapi import APIRouter

from api.achievement.v1.achievement import achievement_router
from api.chat.v1.chat import chat_router
from api.comment.v1.comment import comment_router
from api.user.v1.user import user_router as user_v1_router
from api.event.v1.event import event_router as event_v1_router
from api.auth.auth import auth_router

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(user_v1_router, prefix="/users", tags=["User"])
router_v1.include_router(event_v1_router, prefix="/events", tags=["Event"])
router_v1.include_router(auth_router, prefix="/auth", tags=["Auth"])
router_v1.include_router(chat_router, prefix="/chat", tags=["Chat"])
router_v1.include_router(comment_router, prefix="/comment", tags=["Comment"])
router_v1.include_router(achievement_router, prefix="/achievement", tags=["Achievement"])

router = APIRouter()
router.include_router(router_v1)

__all__ = ["router"]
