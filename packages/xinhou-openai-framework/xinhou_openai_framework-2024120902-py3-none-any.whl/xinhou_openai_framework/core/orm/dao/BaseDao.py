# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   BaseDao.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/6 10:47   shenpeng   1.0         None
"""
from typing import TypeVar, Generic, List

from pydantic import BaseModel
from sqlalchemy import text, desc
from sqlalchemy.orm import Session, Query
from xinhou_openai_framework.pages.Order import Order
from xinhou_openai_framework.pages.PageHelper import PageHelper
from xinhou_openai_framework.pages.Paginate import Paginate

M = TypeVar('M', bound=BaseModel)


class BaseDao(Generic[M]):
    """
    基础Dao服务类
    """
    db: Session = None
    cls = None

    def __init__(self, db: Session, cls=None):
        self.db = db
        if cls is not None:
            # 如果实例化时不传递实体cls类型，则需要手动调用query(User)方法将模型cls传入
            self.cls = cls

    def query(self, cls):
        """
        设置查询模型
        """
        self.cls = cls
        return self

    def conditions(self, model: M):
        """
        组织查询过滤条件
        """
        filters = {}
        keys = model.__dict__.keys()
        values = model.__dict__.values()
        tmp = dict(zip(keys, values))
        for key, value in tmp.items():
            if value is not None and value != "" and key != '_sa_instance_state':
                filters[key] = value
        return filters

    def execute_sql(self, sql, params) -> dict:
        """
        执行原始SQL
        """
        result_proxy = self.db.execute(sql, params)
        row_proxy_list = result_proxy.fetchall()
        if not row_proxy_list:
            return None
        return [dict(zip(result_proxy.keys(), row_proxy)) for row_proxy in row_proxy_list]

    # ===============================================business method====================================================

    def save(self, model: M) -> M:
        """
        根据模型保存数据
        """
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def save_not_commit(self, model: M) -> M:
        """
        根据模型保存数据
        """
        self.db.add(model)
        return model

    def save_all(self, models: List[M]) -> bool:
        """
        批量模型保存数据
        """
        self.db.add_all(models)
        self.db.commit()
        return True

    def save_all_not_commit(self, models: List[M]) -> bool:
        """
        批量模型保存数据
        """
        self.db.add_all(models)
        return True

    def update(self, model: M) -> M:
        """
        根据模型更新数据
        """
        db_model = self.db.merge(model, load=True)
        self.db.commit()
        return db_model

    def update_not_commit(self, model: M) -> M:
        """
        根据模型更新数据
        """
        db_model = self.db.merge(model, load=True)
        return db_model

    def update_all(self, models: List[M]) -> bool:
        """
        批量模型更新数据
        """
        for model in models:
            self.update(model)
        return True

    def update_all_not_commit(self, models: List[M]) -> bool:
        """
        批量模型更新数据
        """
        for model in models:
            self.update_not_commit(model)
        return True

    def delete(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = self.find_by_id(model)
        if not db_model:
            return False
        self.db.delete(db_model)
        self.db.commit()
        return True

    def delete_not_commit(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = self.find_by_id(model)
        if not db_model:
            return False
        self.db.delete(db_model)
        return True

    def delete_by_id(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = self.find_by_id(model)
        if not db_model:
            return False
        self.db.delete(db_model)
        self.db.commit()
        return True

    def delete_by_id_not_commit(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = self.find_by_id(model)
        if not db_model:
            return False
        self.db.delete(db_model)
        return True

    def delete_all(self, models: List[M]):
        """
        批量根据模型删除数据
        """
        for model in models:
            self.delete_by_id(model)
        return True

    def delete_all_not_commit(self, models: List[M]):
        """
        批量根据模型删除数据
        """
        for model in models:
            self.delete_by_id_not_commit(model)
        return True

    def exists(self, model: M) -> bool:
        """
        根据模型查询判断数据是否存在
        """
        cls = type(model)
        query: Query = self.db.query(cls).filter_by(**self.conditions(model))
        return self.db.query(query.exists()).scalar()

    def count(self, model: M) -> int:
        """
        根据模型统计数据条数
        """
        cls = type(model)
        return self.db.query(cls).filter_by(**self.conditions(model)).count()

    def find_by_id(self, model: M) -> M:
        """
        根据模型查询指定ID数据
        """
        return self.db.query(type(model)).get(model.id)

    def find_by_ids(self, ids: List[int], model: M = None) -> List[M]:
        """
        根据模型查询指定ID数据
        """
        if model is None:
            query: Query = self.db.query(self.cls).filter(self.cls.id.in_(ids))
        else:
            query: Query = self.db.query(self.cls).filter(self.cls.id.in_(ids)).filter_by(**self.conditions(model))
        return query.all()

    def find_all(self, model: M, order: Order = None) -> List[M]:
        """
        根据模型查询所有数据，默认按id降序排序
        """
        query: Query = self.db.query(self.cls).filter_by(**self.conditions(model))

        if order is not None:  # 如果提供了自定义排序，则使用自定义排序
            query = query.order_by(text(order.property + " " + order.direction))
        else:  # 否则，默认按id降序排序
            query = query.order_by(desc(self.cls.id))

        return query.all()

    def find_by(self, search: PageHelper[M]) -> Paginate:
        """
        根据模型查询分页数据
        """
        query: Query = self.db.query(self.cls).filter_by(**self.conditions(search.query))
        if search.sorter.orders is not None:  # 组织排序
            for order in search.sorter.orders:
                query = query.order_by(text(order.property + " " + order.direction))
        paginate = Paginate(query, search.pager.page_num, search.pager.page_size, search.sorter.orders)
        return paginate
