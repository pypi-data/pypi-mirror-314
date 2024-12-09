# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   CommonController.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/3/10 00:37   shenpeng   1.0         None
"""
from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

base_common_api = APIRouter()


@base_common_api.api_route('/health', methods=['GET'],
                           tags=["common"],
                           summary="健康检查接口",
                           description="通过此接口判断服务是否正常运行")
async def health():
    logger.info("This server is very health.")
    return JSONResponse({"code": 200, "msg": "This server is very health!"})
