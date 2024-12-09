# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   AppContext.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 14:30   shenpeng   1.0         None
"""

from pydantic import BaseModel

from xinhou_openai_framework.core.context.model.ApplicationConfig import Application
from xinhou_openai_framework.core.context.model.FrameworkConfig import Framework
from xinhou_openai_framework.utils.ObjDictUtil import ObjectDict


class AppContext(BaseModel):

    """
    应用上下文模型
    """
    application: Application = Application()
    framework: Framework = Framework()

    ctx: dict = {}

    def append_dist(self, conf):
        self.ctx = ObjectDict.merge_dicts(self.ctx,conf)
