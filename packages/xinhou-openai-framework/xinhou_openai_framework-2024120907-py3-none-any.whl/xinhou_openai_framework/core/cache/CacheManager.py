# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
缓存管理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   CacheManager.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/4/4 17:34   shenpeng   1.0         None
"""
import json

import redis
from loguru import logger

from xinhou_openai_framework.core.context.model.AppContext import AppContext


class CacheManager:
    _instance = None

    def __init__(self):
        self.__redis = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def connect(self, context: AppContext):
        host = context.framework.redis.host
        port = context.framework.redis.port
        db = context.framework.redis.database
        password = context.framework.redis.password
        self.__redis = redis.Redis(host=host, port=port, db=db, password=password)

    def disconnect(self):
        if self.__redis is not None:
            self.__redis = None

    def set(self, key, value, ex=None):
        try:
            value = json.dumps(value)
            if ex:
                self.__redis.setex(key, ex, value)
            else:
                self.__redis.set(key, value)
            return True
        except Exception as e:
            logger.error(f"设置键值对失败: {e}")
            return False

    def get(self, key):
        try:
            value = self.__redis.get(key)
            if value:
                value = json.loads(value)
            return value
        except Exception as e:
            logger.error(f"获取键值对失败: {e}")
            return None

    def delete(self, *keys):
        try:
            return self.__redis.delete(*keys)
        except Exception as e:
            logger.error(f"删除键值对失败：{e}")
            return 0

    def update(self, key, value):
        try:
            self.__redis.set(key, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"修改键值对失败：{e}")
            return False
