# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   NacosConfig.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 14:48   shenpeng   1.0         None
"""

from typing import Optional, List

from pydantic import BaseModel


class NacosDiscovery(BaseModel):
    server_addr: Optional[str] = None
    namespace_id: Optional[str] = None
    enabled: bool = False
    username: Optional[str] = None
    password: Optional[str] = None
    group: Optional[str] = None


class NacosConfig(BaseModel):
    server_addr: Optional[str] = None
    namespace_id: Optional[str] = None
    enabled: bool = False
    username: Optional[str] = None
    password: Optional[str] = None
    group: Optional[str] = None
    shared_configs: Optional[List[str]] = None


class Nacos(BaseModel):
    discovery: NacosDiscovery = NacosDiscovery()
    config: NacosConfig = NacosConfig()
