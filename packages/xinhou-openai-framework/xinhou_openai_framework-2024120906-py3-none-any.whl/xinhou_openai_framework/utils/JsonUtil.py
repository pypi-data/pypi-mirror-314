# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   JsonUtil.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:17   shenpeng   1.0         None
"""
import json

from loguru import logger


class JsonUtil:
    """
    JSON转换工具类
    """

    @staticmethod
    def object_to_json(obj, indent=None):
        """
        将对象转换为JSON字符串
        :param obj: 对象
        :param indent: 缩进
        :return: JSON字符串
        """
        return json.dumps(obj, default=lambda o: o.__dict__, indent=indent)

    @staticmethod
    def json_to_object(json_data, cls):
        """
        将JSON字符串转换为对象
        :param json_data: JSON字符串
        :return: 对象
        """
        return type(cls, object, **json.loads(json_data))


if __name__ == '__main__':
    # 定义一个对象
    class ClazzDemo:
        def __init__(self, name):
            self.name = name


    class UserDemo:
        def __init__(self, name, age, clazz: ClazzDemo):
            self.name = name
            self.age = age
            self.clazz = clazz


    user = UserDemo("John Doe", 30, ClazzDemo("A班级"))

    # 将对象转换为JSON字符串
    json_data = json.dumps(user, default=lambda o: o.__dict__, indent=4)
    logger.info(json_data)

    # 将JSON字符串转换为对象
    user_demo = UserDemo(**json.loads(json_data))
    logger.info(user_demo)
