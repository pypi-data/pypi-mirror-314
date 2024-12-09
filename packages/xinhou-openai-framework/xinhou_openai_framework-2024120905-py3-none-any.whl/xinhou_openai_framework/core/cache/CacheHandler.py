# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
初始化缓存处理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   CacheHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/4/4 17:33   shenpeng   1.0         None
"""
from xinhou_openai_framework.core.cache.RedisConnectionPool import RedisConnectionPool


class CacheHandler:

    @staticmethod
    def init_cache(app, context):
        @app.on_event("startup")
        async def startup_cache_manager_event():
            # 初始化缓存连接和管理器
            redis_pool = RedisConnectionPool()
            await redis_pool.initialize_ctx_pool(context)

        @app.on_event("shutdown")
        async def shutdown_cache_manager_event():
            # 关闭缓存连接和管理器
            redis_pool = RedisConnectionPool()
            await redis_pool.close_pool()
