# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   marmot-xinhou-openai-framework  
@File    :   QueryUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/28 18:20   shenpeng   1.0         None
"""

from datetime import datetime, date, time
from typing import Any, Dict, List
from pydantic import BaseModel
from sqlalchemy import DateTime, Numeric, Date, Time

from xinhou_openai_framework.core.orm.entity.BaseEntity import BaseEntity


class QueryUtil:

    @staticmethod
    def query_set_to_dict(datas: Any) -> Any:
        if isinstance(datas, list):
            if not datas:
                return []

            first_item = datas[0]
            if isinstance(first_item, BaseModel):
                return [data.model_dump() for data in datas]
            elif isinstance(first_item, dict):
                return QueryUtil._process_dict_list(datas)
            elif isinstance(first_item, BaseEntity):
                return QueryUtil._process_base_entity_list(datas)
            else:
                return QueryUtil._process_any_list(datas)
        else:
            return QueryUtil._process_single_object(datas)

    @staticmethod
    def _process_dict_list(datas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for r in datas:
            QueryUtil._convert_datetime(r)
        return datas

    @staticmethod
    def _process_base_entity_list(datas: List[BaseEntity]) -> List[Dict[str, Any]]:
        return [QueryUtil._base_entity_to_dict(vo) for vo in datas]

    @staticmethod
    def _process_any_list(datas: List[Any]) -> List[Dict[str, Any]]:
        return [dict(zip(data.keys(), data)) for data in datas]

    @staticmethod
    def _process_single_object(datas: Any) -> Dict[str, Any]:
        if isinstance(datas, BaseEntity):
            return QueryUtil._base_entity_to_dict(datas)
        elif isinstance(datas, dict):
            return datas
        else:
            res = dict(zip(datas.keys(), datas))
            QueryUtil._convert_datetime(res)
            return res

    @staticmethod
    def _base_entity_to_dict(model: BaseEntity) -> Dict[str, Any]:
        return dict(QueryUtil.model_to_dict(model))

    @staticmethod
    def model_to_dict(model: BaseEntity) -> Dict[str, Any]:
        for col in model.__table__.columns:
            value = getattr(model, col.name)
            if isinstance(col.type, DateTime):
                value = QueryUtil._convert_datetime(value)
            elif isinstance(col.type, Numeric):
                value = float(value) if value else None
            elif isinstance(col.type, BaseEntity):
                value = QueryUtil.model_to_dict(value)
            yield (col.name, value)

    @staticmethod
    def _convert_datetime(value: Any) -> str:
        if isinstance(value, (datetime, date, time)):
            return value.strftime("%Y-%m-%d %H:%M:%S") if isinstance(value, datetime) else value.strftime("%Y-%m-%d")
        return ""


if __name__ == '__main__':
    # 示例数据
    class BaseEntity:
        def __init__(self, name):
            self.name = name


    class TestModel(BaseEntity):
        pass


    data_list = [TestModel("Test1"), TestModel("Test2"), TestModel("Test3")]

    # 调用示例
    result = QueryUtil.query_set_to_dict(data_list)
    print(result)
