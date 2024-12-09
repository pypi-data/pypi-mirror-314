# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ObjUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/27 10:11   shenpeng   1.0         None
"""
from typing import Iterable

from loguru import logger
from pydantic import BaseModel

from xinhou_openai_framework.utils.ObjDictUtil import ObjectDict


class ObjUtil:

    @staticmethod
    def dict_to_obj(d):
        if isinstance(d, dict):
            n = ObjectDict()
            for k, v in d.items():
                n[k] = ObjUtil.dict_to_obj(v)
            return n
        if isinstance(d, list):
            n = []
            for v in d:
                n.append(ObjUtil.dict_to_obj(v))
            return n
        return d

    # @staticmethod
    # def dict_to_obj(obj: object, **d) -> object:
    #     """
    #     字典转对象
    #     :param obj:
    #     :param dict:
    #     :return:
    #     """
    #     obj.__dict__.update(d)
    #     return obj

    @staticmethod
    def obj_to_dict(obj: object) -> dict:
        """
        对象转字典（单对象）
        :param obj:
        :return:
        """
        # from collections import Iterable
        try:
            if isinstance(obj, Iterable):
                tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in obj]
                for t in tmp:
                    if '_sa_instance_state' in t.keys():
                        t.pop('_sa_instance_state')
            else:
                tmp = dict(zip(obj.__dict__.keys(), obj.__dict__.values()))
                if '_sa_instance_state' in tmp.keys():
                    tmp.pop('_sa_instance_state')
            return tmp
        except BaseException as e:
            logger.error(e.args)
            raise TypeError('Type error of parameter')

    @staticmethod
    def obj_many_to_dict(obj: object) -> dict:
        """
        对象转字典（嵌套对象）
        :param obj:
        :return:
        """
        from collections import Iterable
        try:
            if isinstance(obj, Iterable):
                tmps = []
                for res in obj:
                    tmp = dict(zip(res.__dict__.keys(), res.__dict__.values()))
                    for key, value in tmp.items():
                        if isinstance(value, BaseModel):
                            tmp[key] = ObjUtil.obj_many_to_dict(value)
                    tmp.pop('_sa_instance_state')
                    tmps.append(tmp)
            else:
                tmp = dict(zip(obj.__dict__.keys(), obj.__dict__.values()))
                for key, value in tmp.items():
                    if isinstance(value, BaseModel):
                        tmp[key] = ObjUtil.obj_many_to_dict(value)
                tmp.pop('_sa_instance_state')
            return tmp
        except BaseException as e:
            logger.error(e.args)
            raise TypeError('Type error of parameter')
