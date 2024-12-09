# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ValidateUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/3/28 09:58   shenpeng   1.0         None
"""

import re
from datetime import datetime


class V:
    @staticmethod
    def is_valid_string(value, min_length=None, max_length=None, pattern=None):
        """
        判断字符串是否合法
        :param value: 要验证的字符串
        :param min_length: 字符串最小长度，可以为 None
        :param max_length: 字符串最大长度，可以为 None
        :param pattern: 字符串的正则表达式，可以为 None
        :return: 如果字符串合法则返回 True，否则返回 False
        """
        if not isinstance(value, str):
            return False
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        if pattern is not None and not re.match(pattern, value):
            return False
        return True

    @staticmethod
    def is_valid_int(value, min_value=None, max_value=None):
        """
        判断整数是否合法
        :param value: 要验证的整数
        :param min_value: 整数的最小值，可以为 None
        :param max_value: 整数的最大值，可以为 None
        :return: 如果整数合法则返回 True，否则返回 False
        """
        if not isinstance(value, int):
            return False
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True

    @staticmethod
    def is_valid_float(value, min_value=None, max_value=None):
        """
        判断浮点数是否合法
        :param value: 要验证的浮点数
        :param min_value: 浮点数的最小值，可以为 None
        :param max_value: 浮点数的最大值，可以为 None
        :return: 如果浮点数合法则返回 True，否则返回 False
        """
        if not isinstance(value, float):
            return False
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True

    @staticmethod
    def is_valid_date(value, date_format="%Y-%m-%d"):
        """
        判断日期是否合法
        :param value: 要验证的日期字符串
        :param date_format: 日期字符串的格式，默认为 "%Y-%m-%d"
        :return: 如果日期合法则返回 True，否则返回 False
        """
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_list(value, min_length=None, max_length=None, item_validator=None):
        """
        判断列表是否合法
        :param value: 要验证的列表
        :param min_length: 列表的最小长度，可以为 None
        :param max_length: 列表的最大长度，可以为 None
        :param item_validator: 对列表中每个元素进行验证的函数，可以为 None
            :return: 如果列表合法则返回 True，否则返回 False
        """
        if not isinstance(value, list):
            return False
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        if item_validator is not None:
            for item in value:
                if not item_validator(item):
                    return False
        return True

    @staticmethod
    def is_valid_dict(value, key_validator=None, value_validator=None):
        """
        判断字典是否合法
        :param value: 要验证的字典
        :param key_validator: 对字典的 key 进行验证的函数，可以为 None
        :param value_validator: 对字典的 value 进行验证的函数，可以为 None
        :return: 如果字典合法则返回 True，否则返回 False
        """
        if not isinstance(value, dict):
            return False
        if key_validator is not None:
            for key in value.keys():
                if not key_validator(key):
                    return False
        if value_validator is not None:
            for val in value.values():
                if not value_validator(val):
                    return False
        return True

    @staticmethod
    def is_valid_set(value, min_length=None, max_length=None, item_validator=None):
        """
        判断集合是否合法
        :param value: 要验证的集合
        :param min_length: 集合的最小长度，可以为 None
        :param max_length: 集合的最大长度，可以为 None
        :param item_validator: 对集合中每个元素进行验证的函数，可以为 None
        :return: 如果集合合法则返回 True，否则返回 False
        """
        if not isinstance(value, set):
            return False
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        if item_validator is not None:
            for item in value:
                if not item_validator(item):
                    return False
        return True

    @staticmethod
    def is_valid_phone_number(value):
        """
        判断电话号码是否合法
        :param value: 要验证的电话号码
        :return: 如果电话号码合法则返回 True，否则返回 False
        """
        pattern = r'^0\d{2,3}-?\d{7,8}$'
        return re.match(pattern, value) is not None

    @staticmethod
    def is_valid_mobile_number(value):
        """
        判断手机号码是否合法
        :param value: 要验证的手机号码
        :return: 如果手机号码合法则返回 True，否则返回 False
        """
        pattern = r'^1[3456789]\d{9}$'
        return re.match(pattern, value) is not None

    @staticmethod
    def is_valid_md5(value):
        """
        判断 MD5 是否合法
        :param value: 要验证的 MD5 值
        :return: 如果 MD5 合法则返回 True，否则返回 False
        """
        pattern = r'^[0-9a-f]{32}$'
        return re.match(pattern, value) is not None
