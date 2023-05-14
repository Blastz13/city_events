from fastapi import APIRouter, Response, Depends

from core.fastapi.dependencies import PermissionDependency, AllowAll
from core.helpers.redis import redis_client
import logging

health_router = APIRouter(prefix="/health", tags=["Health"])

logger = logging.getLogger("app")


@health_router.get("/", dependencies=[Depends(PermissionDependency([AllowAll]))])
async def app_healthcheck():
    return Response(status_code=200)


@health_router.get("/sentry")
async def sentry_healthcheck():
    1 / 0


@health_router.get("/mongo", status_code=200)
async def mongo_healthcheck():
    from core.db.mongo_db import client
    try:
        client.admin.command('ping')
        return {"message": "MongoDB is up"}
    except Exception as ex:
        logger.error(ex)
        return {"message": "MongoDB is down"}


@health_router.get("/elastic", status_code=200)
async def elastic_healthcheck():
    from core.db.elastic_db import es_client
    try:
        await es_client.ping()
        return {"message": "Elasticsearch is up"}
    except Exception as ex:
        logger.error(ex)
        return {"message": "Elasticsearch is down"}


@health_router.get("/redis", status_code=200)
async def redis_healthcheck():
    try:
        await redis_client.ping()
        return {"message": "Redis is up"}
    except Exception as ex:
        logger.error(ex)
        return {"message": "Redis is down"}
