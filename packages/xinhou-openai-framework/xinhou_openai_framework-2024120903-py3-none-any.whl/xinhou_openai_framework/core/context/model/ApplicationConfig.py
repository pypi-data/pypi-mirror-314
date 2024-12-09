# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ApplicationConfig.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 14:44   shenpeng   1.0         None
"""
from typing import Optional

from pydantic import BaseModel


class Server(BaseModel):
    """
    服务信息模型
    """
    host: Optional[str] = None
    post: Optional[int] = None
    context_path: Optional[str] = None
    reload: Optional[bool] = True
    debug: Optional[bool] = True
    is_proxy: Optional[bool] = False


class License(BaseModel):
    """
    证书信息模型
    """
    name: Optional[str] = None
    url: Optional[str] = None


class Application(BaseModel):
    """
    应用信息模型
    """
    name: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    email: Optional[str] = None
    license: License = License()
    server: Server = Server()
