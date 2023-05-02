from fastapi import APIRouter, Response, Depends

from core.fastapi.dependencies import PermissionDependency, AllowAll
from logging import getLogger

home_router = APIRouter()

logger = getLogger('app')


@home_router.get("/health", dependencies=[Depends(PermissionDependency([AllowAll]))])
async def home():
    logger.info("Hello world!")
    return Response(status_code=200)


@home_router.get("/sentry-debug")
async def trigger_error():
    1 / 0
