# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
代码生成参数模型
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   GenerateCodeSchema.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/3/26 18:06   shenpeng   1.0         None
"""
from typing import Optional, List

from pydantic import BaseModel, Field


class GenerateCodeSchema(BaseModel):
    tables_white: List[str] = Field(
        title="白名单列表"
    )

    ignore_fields: List[str] = Field(
        title="忽略字段列表"
    )
