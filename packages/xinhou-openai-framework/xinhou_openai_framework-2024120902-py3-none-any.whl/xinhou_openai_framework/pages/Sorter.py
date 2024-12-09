# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   Sorter.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:44   shenpeng   1.0         None
"""
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.v1 import Required

from xinhou_openai_framework.pages.Order import Order


class Sorter(BaseModel):
    orders: Optional[List[Order]] = Field(default=Required, title="排序条件集合")

    @classmethod
    def new(cls, **kwargs):
        orders_list: List[Order] = []
        for order in kwargs.get("orders"):
            orders_list.append(Order.new(**order))
        return Sorter(orders_list)
