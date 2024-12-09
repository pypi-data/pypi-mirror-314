# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   RedisUtil.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:17   shenpeng   1.0         None
"""

import json
import redis
from loguru import logger


class RedisUtil:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """
        初始化Redis连接
        :param host: Redis地址，默认为localhost
        :param port: Redis端口，默认为6379
        :param db: Redis数据库编号，默认为0
        :param password: Redis密码，默认为None
        """
        self.__redis = redis.Redis(host=host, port=port, db=db, password=password)

    def set(self, key, value, ex=None):
        """
        将值value关联到key，如果key已经持有其他值，SET就覆写旧值，无视类型
        :param key: 待存储的键
        :param value: 待存储的值
        :param ex: 过期时间（单位：秒），默认为None，即不过期
        :return: 返回True表示存储成功，否则返回False
        """
        try:
            value = json.dumps(value)
            if ex:
                self.__redis.setex(key, value, ex)
            else:
                self.__redis.set(key, value)
            return True
        except Exception as e:
            logger.error("设置键值对失败: ", e)
            return False

    def get(self, key):
        """
        获取与key关联的值
        :param key: 待获取的键
        :return: 返回key对应的值，如果key不存在，返回None
        """
        try:
            value = self.__redis.get(key)
            if value:
                value = json.loads(value)
            return value
        except Exception as e:
            logger.error("获取键值对失败: ", e)
            return None

    def delete(self, *keys):
        """
        删除指定键值对
        :param keys: 需要删除的键，多个键用逗号分隔
        :return: 被删除的键值对数量
        """
        try:
            return self.__redis.delete(*keys)
        except Exception as e:
            logger.error(f"删除键值对失败：{e}")
            return 0

    def update(self, key, value):
        """
        修改键值对
        :param key: 键
        :param value: 值，字典、列表、数字等类型
        :return: 修改成功返回True，失败返回False
        """
        try:
            self.__redis.set(key, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"修改键值对失败：{e}")
            return False

    def publish_message(self, channel, message):
        """
        将消息发布到指定频道
        :param channel: 频道名称
        :param message: 要发布的消息
        :return: 成功发布的消息数量
        """
        try:
            return self.__redis.publish(channel, json.dumps(message))
        except Exception as e:
            logger.error("消息发布失败: ", e)
            return 0

    def subscribe(self, channel):
        """
        订阅指定频道
        :param channel: 频道名称
        :return: PubSub对象
        """
        pubsub = self.__redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def listen_for_messages(self, pubsub):
        """
        持续监听订阅的频道，并处理接收到的消息
        :param pubsub: PubSub对象
        """
        while True:
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                logger.error("Received message:", message['data'])
                # 处理消息后确认消息已接收
                # ...


if __name__ == '__main__':
    redis_util = RedisUtil(host="101.132.165.205", port="36379")

    # 消息推送
    channel = 'my_channel'
    message = {'key': 'value'}
    result = redis_util.publish_message(channel, message)
    logger.info("123")
    # # 消息接收及确认
    # pubsub = redis_util.subscribe(channel)
    # redis_util.listen_for_messages(pubsub)

    # key = Md5Util.md5_string("test")
    # value = {
    #     "name": "Tom",
    #     "age": 20
    # }
    # redis_util.set(key, value)
    # logger.info(redis_util.get(key))
    # redis_util.update(key, {'name': 'Tom123', 'age': 25})
    # logger.info(redis_util.get(key))
    # redis_util.delete(key)
    # logger.info(redis_util.get(key))
