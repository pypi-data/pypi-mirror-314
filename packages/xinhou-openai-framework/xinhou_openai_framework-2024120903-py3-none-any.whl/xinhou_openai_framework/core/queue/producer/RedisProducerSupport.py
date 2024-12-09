import asyncio
import json
from typing import List

from loguru import logger

from xinhou_openai_framework.core.cache.RedisConnectionPool import RedisConnectionPool
from xinhou_openai_framework.core.exception.GlobalBusinessException import GlobalBusinessException
from xinhou_openai_framework.core.queue.message.RedisMessageModel import RedisMessageModel
from xinhou_openai_framework.utils.DateUtil import DateUtil
from xinhou_openai_framework.utils.IdUtil import IdUtil


class RedisProducerSupport:
    def __init__(self, redis_pool, queue_name='xinhou_queue'):
        self.redis = redis_pool
        self.queue_name = queue_name

    async def add_messages_to_queue(self, messages: List[RedisMessageModel]):
        try:
            serialized_messages = [message.model_dump_json() for message in messages]
            result = await self.redis.lpush(self.queue_name, *serialized_messages)
            logger.info(f'生产者已发送消息到队列[{self.queue_name}]，现有队列中消息数量为[{result}]条')
        except Exception as e:
            logger.error("生产者发送消息时发生异常")
            logger.error(e)
            raise GlobalBusinessException(500, "生产者发送消息时发生异常")

    async def get_all_messages_from_queue(self):
        try:
            all_messages = await self.redis.lrange(f"{self.queue_name}_fail", 0, -1)
            return all_messages
        except Exception as e:
            logger.error(f"生产者获取[{self.queue_name}_fail]失败消息时发生异常")
            logger.error(e)
            raise GlobalBusinessException(500, f"生产者获取[{self.queue_name}_fail]失败消息时发生异常")

    async def remove_message_by_key(self, key):
        try:
            all_messages = await self.redis.lrange(f"{self.queue_name}_fail", 0, -1)
            for message in all_messages:
                msg = json.loads(message)
                if msg.get('key') == key:
                    await self.redis.lrem(f"{self.queue_name}_fail", 0, message)
                    logger.info(f'生产者已删除在队列[{self.queue_name}_fail]中的[{key}]失败消息')
                    break
        except Exception as e:
            logger.error(f"生产者删除[{key}]失败消息时发生异常")
            logger.error(e)
            raise GlobalBusinessException(500, f"生产者删除[{key}]失败消息时发生异常")


class ProducerServiceSupport(RedisProducerSupport):

    @staticmethod
    async def process_push(queue_name, messages: List[RedisMessageModel]):
        redis_pool = await RedisConnectionPool().get_pool()
        redis_producer = ProducerServiceSupport(**{
            "redis_pool": redis_pool,
            "queue_name": queue_name
        })
        await redis_producer.add_messages_to_queue(messages)

    @staticmethod
    async def get_all_fail_messages(queue_name) -> List[RedisMessageModel]:
        redis_pool = await RedisConnectionPool().get_pool()
        all_fail_messages = await ProducerServiceSupport(**{
            "redis_pool": redis_pool,
            "queue_name": queue_name
        }).get_all_messages_from_queue()

        fail_messages = []
        for message in all_fail_messages:
            fail_messages.append(RedisMessageModel(**json.loads(message)))
        return fail_messages

    @staticmethod
    async def remove_by_key(queue_name, key):
        redis_pool = await RedisConnectionPool().get_pool()
        await ProducerServiceSupport(**{
            "redis_pool": redis_pool,
            "queue_name": queue_name
        }).remove_message_by_key(key)


async def producer_process_push(content):
    redis_pool = await RedisConnectionPool().get_pool()
    cfg = {
        "redis_pool": redis_pool,
        "queue_name": 'xinhou_queue'
    }
    redis_producer = RedisProducerSupport(**cfg)

    # content = V5ReqTrainingStreamSummarySchema(**{
    #     "question": "请总结问答内容",
    #     "prompt_template": "请根据上下文内容总结相关数据",
    #     "history_file_oss_object_key": "/static/public/upload/1.txt",
    #     "max_length": 500,
    #     "steam_wrap": "<br/>"
    # })

    await redis_producer.add_messages_to_queue([
        RedisMessageModel(key=IdUtil.uuid_32(), content=content, timestamp=DateUtil.get_current_timestamp())
    ])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    redis_connection = RedisConnectionPool()
    loop.run_until_complete(redis_connection.initialize_pool('101.132.165.205', 36379))
    # 执行 producer_process_push() 函数 20 次
    for _ in range(20):
        loop.run_until_complete(producer_process_push())
    loop.close()
