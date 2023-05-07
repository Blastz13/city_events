import motor.motor_asyncio

from core.config import config

MONGO_DETAILS = f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client["event_city_chat"]
