from src.app.infrastructure.cache.accessor import get_redis_connection


class RedisTools:
    _redis_connect = get_redis_connection()

    @classmethod
    async def set_pair(cls, key, value):
        await cls._redis_connect.set(key, value)

    @classmethod
    async def get_pair(cls, key):
        if key is not None:
            result = await cls._redis_connect.get(key)
            return result

    @classmethod
    async def get_keys(cls):
        all_keys = await cls._redis_connect.keys(pattern='*')
        return all_keys

    @classmethod
    async def delete_key(cls, key=None):
        if key is not None:
            await cls._redis_connect.delete(key)
        else:
            await cls._redis_connect.flushdb()
