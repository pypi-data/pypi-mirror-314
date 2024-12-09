# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   Pager.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:42   shenpeng   1.0         None
"""
from typing import Optional

from pydantic import BaseModel, Field

from xinhou_openai_framework.utils.ObjUtil import ObjUtil


class Pager(BaseModel):
    page_num: Optional[int] = Field(title="当前页")
    page_size: Optional[int] = Field(title="每页记录数")
    total_page: Optional[int] = Field(None, title="总页数")
    total_record: Optional[int] = Field(None, title="总记录数")

    @classmethod
    def new(cls, **kwargs):
        return ObjUtil.dict_to_obj(cls(), **kwargs)
