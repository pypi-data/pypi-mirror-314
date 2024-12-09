from aioredis import create_redis_pool

from xinhou_openai_framework.core.context.model.AppContext import AppContext


class RedisConnectionPool:
    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize_pool(self, redis_ip='127.0.0.1', redis_port=6379, db=0):
        self._pool = await create_redis_pool(f'redis://{redis_ip}:{redis_port}', db=db)

    async def initialize_ctx_pool(self, context: AppContext):
        try:
            self._pool = await create_redis_pool(
                f'redis://{context.framework.redis.host}:{context.framework.redis.port}',
                db=context.framework.redis.database)
        except Exception as ex:
            self._pool = await create_redis_pool(
                f'redis://{context.framework.redis.host}:{context.framework.redis.port}',
                db=context.framework.redis.database,
                password=context.framework.redis.password)

    @classmethod
    def set_instance(cls, instance):
        cls._instance = instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Redis pool has not been initialized.")
        return cls._instance

    async def get_pool(self):
        if self._pool is None:
            raise RuntimeError("Redis pool has not been initialized.")
        return self._pool

    async def close_pool(self):
        if self._pool is not None:
            self._pool.close()
            await self._pool.wait_closed()
