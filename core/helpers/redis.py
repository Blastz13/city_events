import redis.asyncio as aioredis

from core.config import config

redis_client = aioredis.from_url(url=f"redis://{config.REDIS_HOST}")
