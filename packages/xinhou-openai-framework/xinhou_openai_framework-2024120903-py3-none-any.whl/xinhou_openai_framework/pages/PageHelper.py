# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   PageHelper.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:17   shenpeng   1.0         None
"""
from typing import Optional, TypeVar, Generic, List

from pydantic import Field, BaseModel
from pydantic.v1 import Required

from xinhou_openai_framework.pages.Pager import Pager
from xinhou_openai_framework.pages.Sorter import Sorter

M = TypeVar('M')


class PageHelper(BaseModel, Generic[M]):
    """
    分页查询条件
    """
    query: Optional[M] = Field(default=Required, title="查询条件")
    pager: Optional[Pager] = Field(default=Required, title="分页条件")
    sorter: Optional[Sorter] = Field(default=Required, title="排序条件")


class PageResultHelper(BaseModel, Generic[M]):
    """
    分页查询返回结果
    """
    content: Optional[List[M]] = Field(default=Required, title="返回数据集合")
    pager: Optional[Pager] = Field(default=Required, title="分页条件")
    sorter: Optional[Sorter] = Field(default=Required, title="排序条件")
