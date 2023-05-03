import asyncio

from elasticsearch import AsyncElasticsearch


ELASTICSEARCH_HOSTS = ["http://localhost:9200"]
ELASTICSEARCH_INDEX = "events"

es_client = AsyncElasticsearch(hosts=ELASTICSEARCH_HOSTS)


async def init_elastic():
    if not await es_client.indices.exists(index=ELASTICSEARCH_INDEX):
        await es_client.indices.create(index=ELASTICSEARCH_INDEX, body={
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "description": {"type": "text"}
                }
            }
        })

loop = asyncio.get_event_loop()
loop.create_task(init_elastic())
