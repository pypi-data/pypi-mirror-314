# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
代码生成参数模型
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   GenerateCodeSchema.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/3/26 18:06   shenpeng   1.0         None
"""
from typing import Optional, List

from pydantic import BaseModel, Field


class GenerateCodeSchema(BaseModel):
    project_name: Optional[str] = Field(
        title="项目名称"
    )
    module_name: Optional[str] = Field(
        title="模块名称"
    )
    package_model: Optional[str] = Field(
        title="模型类包"
    )
    package_schema: Optional[str] = Field(
        title="参数类包"
    )
    package_service: Optional[str] = Field(
        title="服务类包"
    )
    package_controller: Optional[str] = Field(
        title="控制器类包"
    )
