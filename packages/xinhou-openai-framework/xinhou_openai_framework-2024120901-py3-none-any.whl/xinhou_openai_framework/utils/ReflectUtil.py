# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   ReflectUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 13:22   shenpeng   1.0         None
"""
from loguru import logger


class ReflectUtil:
    @staticmethod
    def get_class_name(obj):
        """
        获取对象的类名
        :param obj: 任意对象
        :return: 类名
        """
        return obj.__class__.__name__

    @staticmethod
    def get_class_full_name(obj):
        """
        获取对象的完整类名
        :param obj: 任意对象
        :return: 完整类名
        """
        return obj.__class__.__module__ + "." + obj.__class__.__name__

    @staticmethod
    def get_class_fields(obj):
        """
        获取对象的字段名称列表
        :param obj: 任意对象
        :return: 字段名称列表
        """
        return [f for f in obj.__dict__.keys() if not callable(getattr(obj, f)) and not f.startswith("__")]

    @staticmethod
    def get_field_value(obj, field_name):
        """
        获取对象指定字段的值
        :param obj: 任意对象
        :param field_name: 字段名
        :return: 字段值
        """
        return getattr(obj, field_name)

    @staticmethod
    def set_field_value(obj, field_name, value):
        """
        设置对象指定字段的值
        :param obj: 任意对象
        :param field_name: 字段名
        :param value: 值
        """
        setattr(obj, field_name, value)


if __name__ == '__main__':
    class TestClass:
        def __init__(self):
            self.field_a = 123
            self.field_b = "hello world"


    obj = TestClass()

    logger.info(f"Class Name:{ReflectUtil.get_class_name(obj)}")
    logger.info(f"Full Class Name:{ReflectUtil.get_class_full_name(obj)}")
    logger.info(f"Fields:{ReflectUtil.get_class_fields(obj)}")
    logger.info(f"Field Value:{ReflectUtil.get_field_value(obj, 'field_a')}")

    ReflectUtil.set_field_value(obj, 'field_a', 456)
    logger.info(f"Field Value:{ReflectUtil.get_field_value(obj, 'field_a')}")
