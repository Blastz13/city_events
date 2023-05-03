import redis
from fastapi import APIRouter, Response, Depends

from core.fastapi.dependencies import PermissionDependency, AllowAll
from core.helpers.redis import redis_client

health_router = APIRouter()


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
    except:
        return {"message": "MongoDB is down"}


@health_router.get("/elastic", status_code=200)
async def elastic_healthcheck():
    from core.db.elastic_db import es_client
    try:
        await es_client.ping()
        return {"message": "Elasticsearch is up"}
    except:
        return {"message": "Elasticsearch is down"}


@health_router.get("/redis", status_code=200)
async def redis_healthcheck():
    try:
        redis_client.ping()
        return {"message": "Redis is up"}
    except:
        return {"message": f"Redis is down"}
