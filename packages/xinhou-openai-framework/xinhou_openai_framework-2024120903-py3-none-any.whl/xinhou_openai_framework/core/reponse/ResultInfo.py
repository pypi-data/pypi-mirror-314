# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   marmot-xinhou-openai-framework  
@File    :   ResultInfo.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/25 17:51   shenpeng   1.0         None
"""
from typing import Dict


class ResultInfo:

    @staticmethod
    def success(data: Dict):
        return {
            "code": 200,
            "msg": "执行业务成功",
            "data": data
        }

    @staticmethod
    def fail(msg: str = None):
        return {
            "code": 500,
            "msg": msg,
            "data": None
        }
