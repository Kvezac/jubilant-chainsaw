from redis import asyncio as redis
from src.app.config import settings


def get_redis_connection() -> redis.Redis:
    setting = settings
    return redis.from_url(setting.get_redis_url)
