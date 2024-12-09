# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   FrameworkConfig.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 14:48   shenpeng   1.0         None
"""

from typing import Optional

from pydantic import BaseModel

from xinhou_openai_framework.core.context.model.NacosConfig import Nacos


class Profiles(BaseModel):
    active: Optional[str] = 'dev'

class Cloud(BaseModel):
    nacos:Nacos = Nacos()


class Pool(BaseModel):
    pool_pre_ping: Optional[bool] = True
    pool_size: Optional[int] = 10
    pool_timeout: Optional[int] = 60
    echo: Optional[bool] = False


class Datasource(BaseModel):
    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    pool: Pool = Pool()


class Redis(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[int] = None
    password: Optional[str] = None
    timeout: Optional[str] = None


class Cache(BaseModel):
    type: Optional[str] = None


class Logs(BaseModel):
    path: Optional[str] = None
    level: Optional[str] = None
    rotation: Optional[str] = None
    enqueue: Optional[bool] = None
    serialize: Optional[bool] = None
    encoding: Optional[str] = None
    retention: Optional[str] = None


class Framework(BaseModel):
    profiles: Optional[Profiles] = Profiles()
    cloud: Optional[Cloud] = Cloud()
    logging: Logs = Logs()
    datasource: Datasource = Datasource()
    redis: Redis = Redis()
    cache: Cache = Cache()
