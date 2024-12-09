# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局响应模型
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ResModel.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/7/12 12:55   shenpeng   1.0         None
"""
from typing import TypeVar, Generic, Optional

from pydantic import Field, BaseModel
from pydantic.v1 import Required

M = TypeVar('M')


class ResModel(BaseModel, Generic[M]):
    """
    通用返回模型
    """

    code: Optional[int] = Field(default=Required, title="编码", description="返回请求编码")
    msg: Optional[str] = Field(default=Required, title="消息", description="返回请求消息")
    data: Optional[M] = Field(default=None, title="内容", description="返回内容")
