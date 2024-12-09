# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
初始化全局配置功能
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ContextHandler.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/3 11:21   shenpeng   1.0         None
"""
from typing import Any

from xinhou_openai_framework.core.context.model.SystemContext import ctx


class ContextHandler:
    """
    上下文处理类
    """

    @staticmethod
    def init_ctx(app, context):
        ctx.__setattr__("context", context)  # 设置全局变量

    @staticmethod
    def get_value(key: str) -> Any:
        if key is not None:
            return ctx.__getattr__(key)

    @staticmethod
    def set_value(key: str, value: dict) -> Any:
        if key is not None and value is not None:
            ctx.__setattr__(key, value)
