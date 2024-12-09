# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局应用初始化代理类
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   InitializeHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/12/28 13:43   shenpeng   1.0         None
"""
import asyncio

from loguru import logger

from xinhou_openai_framework.core.context.model.AppContext import AppContext


async def start_queue_listener(listener_name):
    # 获取全局符号表中对应的方法
    listener_func = globals().get(listener_name)

    # 检查方法是否存在并且可调用
    if listener_func and callable(listener_func):
        # 如果存在且可调用，则创建一个异步任务来执行该方法
        asyncio.create_task(listener_func())
    else:
        logger.info(f"queue listener function [{listener_name}] not found or not callable.")


class QueueListenerHandler:
    """
    应用初始化处理类
    """

    @staticmethod
    def init_listeners(app, context: AppContext):
        @app.on_event("startup")
        async def startup_queue_listeners():
            # 遍历字符串列表，依次调用方法【通过函数方式启动监听器】
            listeners = ['openai_summary_consumer_listener']
            for listener in listeners:
                await start_queue_listener(listener)
