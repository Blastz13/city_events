import asyncio

from elasticsearch import AsyncElasticsearch

from core.config import config

ELASTICSEARCH_HOSTS = [f"http://{config.ELASTICSEARCH_HOSTS}:{config.ELASTICSEARCH_PORT}"]

es_client = AsyncElasticsearch(hosts=ELASTICSEARCH_HOSTS)


async def init_elastic():
    if not await es_client.indices.exists(index=config.ELASTICSEARCH_INDEX):
        await es_client.indices.create(index=config.ELASTICSEARCH_INDEX, body={
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "date_start": {"type": "date"}
                }
            }
        })

loop = asyncio.get_event_loop()
loop.create_task(init_elastic())
