# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ObjDictUtil.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/27 10:11   shenpeng   1.0         None
"""
import json
from typing import TypeVar, Union

from loguru import logger

T = TypeVar('T')


class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            return super(ObjectDict, self).__getattribute__(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            super(ObjectDict, self).__delattr__(name)

    def __repr__(self):
        return f"ObjectDict({super(ObjectDict, self).__repr__()})"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_dict(cls, data: dict) -> 'ObjectDict':
        if not isinstance(data, dict):
            return data
        obj_dict = cls()
        for key, value in data.items():
            obj_dict[key] = cls.from_dict(value)
        return obj_dict

    @classmethod
    def from_str(cls, data: Union[str, bytes]) -> 'ObjectDict':
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return cls.from_dict(json.loads(data))

    @staticmethod
    def merge_dicts(dict1, dict2):
        """
        递归合并两个字典
        """
        merged_dict = dict1.copy()

        for key, value in dict2.items():
            if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
                # 如果都是字典，则递归合并
                merged_dict[key] = ObjectDict.merge_dicts(merged_dict[key], value)
            else:
                # 否则直接更新或添加键值对
                merged_dict[key] = value

        return merged_dict


if __name__ == '__main__':
    data = {
        'name': 'John',
        'age': 25,
        'address': {
            'street': '123 Main St',
            'city': 'New York'
        }
    }

    obj = ObjectDict.from_dict(data)
    logger.info(obj.name)  # 输出: John
    logger.info(obj.age)  # 输出: 25
    logger.info(obj.address.street)  # 输出: 123 Main St
    logger.info(obj.address.city)  # 输出: New York
