# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   BaseTenantEntity.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/6 15:06   shenpeng   1.0         None
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from xinhou_openai_framework.core.orm.entity.BaseEntity import BaseEntity


class BaseTenantEntity(BaseEntity):
    """
    实体基类（持久化模型由此类继承）
    """
    __abstract__ = True  ## 声明当前类为抽象类，被继承，调用不会被创建
    tenant_id = Column(Integer, comment="租户ID")
