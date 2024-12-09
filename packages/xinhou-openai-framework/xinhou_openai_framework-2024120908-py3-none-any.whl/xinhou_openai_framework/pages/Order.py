# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   Order.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:44   shenpeng   1.0         None
"""
from typing import Optional

from pydantic import BaseModel, Field

from xinhou_openai_framework.utils.ObjUtil import ObjUtil


class Order(BaseModel):
    property: Optional[str] = Field(None, title="排序字段")
    direction: Optional[str] = Field(None, title="排序条件", description="排序:asc=升序,desc=降序")

    @classmethod
    def new(cls, **kwargs):
        return ObjUtil.dict_to_obj(cls(), **kwargs)
