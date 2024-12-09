# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   RedisMessager.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/23 18:49   shenpeng   1.0         None
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RedisMessageModel(BaseModel):
    key: str = Field(title="消息KEY")
    content: object = Field(title="消息内容")
    timestamp: datetime = Field(title="消息时间戳")
    err_cause: Optional[str] = Field(default=None, title="消息处理错误原因")
