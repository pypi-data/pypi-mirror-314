# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   RedisConsumer.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/23 18:49   shenpeng   1.0         None
"""

import asyncio
import json

import aiohttp
from loguru import logger

from xinhou_openai_framework.core.cache.RedisConnectionPool import RedisConnectionPool
from xinhou_openai_framework.core.queue.message.RedisMessageModel import RedisMessageModel


class RedisConsumerSupport:
    def __init__(self, redis_pool, queue_name='xinhou_queue', lock_name='xinhou_queue_lock', retry_interval=5,
                 max_retries=3):
        self.redis = redis_pool
        self.queue_name = queue_name
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        if lock_name is None:
            self.lock_name = f"{queue_name}_lock"
        else:
            self.lock_name = lock_name

    async def acquire_lock(self):
        # 使用带有超时的Redis锁
        acquired = await self.redis.execute('SET', self.lock_name, 'locked', 'NX', 'EX', 30)
        return acquired == b'OK'

    async def release_lock(self):
        await self.redis.delete(self.lock_name)

    async def process_message(self, message):
        # 处理消息的逻辑
        logger.info(f"处理消息：{message}")
        await asyncio.sleep(2)  # 模拟处理消息所需的时间

    async def handler(self):
        try:
            while True:
                lock_acquired = await self.acquire_lock()
                if lock_acquired:
                    message = await self.redis.rpop(self.queue_name)
                    if message:
                        success = False
                        msg = RedisMessageModel(**json.loads(message))
                        while not success:
                            try:
                                await asyncio.gather(
                                    self.process_message(msg),
                                    self.redis.lrem(self.queue_name, 0, message)  # 确认消息已被消费，从队列中删除已处理的消息
                                )
                                success = True
                            except Exception as e:
                                logger.error(
                                    f"消费者处理[{msg.key}]消息时发生异常，异常原因:{str(e)},开始调用回调接口")
                                msg.err_cause = str(e)
                                await self.redis.lpush(f"{self.queue_name}_fail", msg.model_dump_json())
                                logger.info(f'消费者已将消息转移到[{self.queue_name}_fail]失败队列中！')
                                # 检查callback_url是否存在
                                callback_url = msg.content.get('callback_url')
                                if callback_url:
                                    # 创建HTTP的POST请求
                                    async with aiohttp.ClientSession() as session:
                                        payload = {"process_key": msg.key,
                                                   "process_result": str(msg.content), "process_error": msg.err_cause,
                                                   "process_success": False}
                                        async with session.post(callback_url, json=payload) as response:
                                            # 你可以添加代码处理响应，如检查HTTP状态码，解析返回的JSON数据等
                                            print(await response.text())
                                else:
                                    logger.info("没有提供回调URL，跳过回调")
                                break

                await self.release_lock()
                await asyncio.sleep(5)

        except asyncio.CancelledError:
            await self.release_lock()
        except Exception as e:
            logger.error("消费者接收消息时发生异常")
            logger.error(e)
        finally:
            await self.release_lock()


class ConsumerServiceSupport(RedisConsumerSupport):
    async def process_message(self, message: RedisMessageModel):
        """
        业务逻辑可以通过继承ConsumerServiceSupport重写process_message用于接收消息及执行业务逻辑
        """
        # 这里实现具体的消息处理逻辑
        logger.info(f"消费者执行业务逻辑: {message.content} : {message.timestamp} ")
        # 可以在这里添加自定义的消息处理逻辑

    @staticmethod
    async def process_listener():
        """
        [启动消息监听器 方法一]业务逻辑可以通过继承ConsumerServiceSupport重写process_listener用于启动消费者监听器
        """
        logger.info("启动消费者[ConsumerServiceSupport]监听")
        redis_pool = await RedisConnectionPool().get_pool()
        await ConsumerServiceSupport(**{
            "redis_pool": redis_pool,
            "queue_name": 'xinhou_queue',
            "lock_name": 'xinhou_queue_lock',
            "retry_interval": 5,
            "max_retries": 3
        }).handler()


async def consumer_process_listener():
    """
    [启动消息监听器 方法二]业务逻辑可以通过consumer_process_listener用于启动消费者监听器
    """
    logger.info("启动消费者[ConsumerServiceSupport]监听")
    redis_pool = await RedisConnectionPool().get_pool()
    await ConsumerServiceSupport(**{
        "redis_pool": redis_pool,
        "queue_name": 'openai_summary_queue',
        "lock_name": 'xinhou_queue_lock',
        "retry_interval": 5,
        "max_retries": 3
    }).handler()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    redis_connection = RedisConnectionPool()
    loop.run_until_complete(redis_connection.initialize_pool('101.132.165.205', 36379, db=8))
    loop.run_until_complete(consumer_process_listener())
    loop.close()
