# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   BaseService.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/6 10:47   shenpeng   1.0         None
"""
from typing import TypeVar, Generic, List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from xinhou_openai_framework.core.db.DatabaseManager import DatabaseManager
from xinhou_openai_framework.core.orm.dao.BaseDao import BaseDao
from xinhou_openai_framework.pages.Order import Order
from xinhou_openai_framework.pages.PageHelper import PageHelper
from xinhou_openai_framework.pages.Paginate import Paginate

M = TypeVar('M', bound=BaseModel)


class BaseServiceImpl(Generic[M]):
    """
    基础Service服务类
    """
    db: Session = None
    dao: BaseDao = None
    cls = None

    def __init__(self, db: Session = None, cls=None, dao: BaseDao = None):
        if db is None:
            db_manager = DatabaseManager.get_instance()
            self.db = db_manager.get_session()
        else:
            self.db = db
        if cls is not None:
            # 如果实例化时不传递实体cls类型，则需要手动调用query(User)方法将模型cls传入
            self.cls = cls
        if dao is not None:
            self.dao = dao
        else:
            self.dao = BaseDao(self.db, cls)

    def query(self, cls):
        """
        设置查询模型
        """
        if cls is not None:
            # 如果实例化时不传递实体cls类型，则需要手动调用query(User)方法将模型cls传入
            self.cls = cls
        return self

    def save(self, model: M) -> M:
        """
        根据模型保存数据
        """
        return self.dao.save(model)

    def save_not_commit(self, model: M) -> M:
        """
        根据模型保存数据
        """
        return self.dao.save_not_commit(model)

    def save_all(self, models: List[M]) -> bool:
        """
        批量模型保存数据
        """
        return self.dao.save_all(models)

    def save_all_not_commit(self, models: List[M]) -> bool:
        """
        批量模型保存数据
        """
        return self.dao.save_save_all_not_commitall(models)

    def update(self, model: M) -> M:
        """
        根据模型更新数据
        """
        return self.dao.update(model)

    def update_not_commit(self, model: M) -> M:
        """
        根据模型更新数据
        """
        return self.dao.update_not_commit(model)

    def update_all(self, models: List[M]) -> bool:
        """
        批量模型更新数据
        """
        return self.dao.update_all(models)

    def update_all_not_commit(self, models: List[M]) -> bool:
        """
        批量模型更新数据
        """
        return self.dao.update_all_not_commit(models)

    def delete(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        return self.dao.delete(model)

    def delete_by_id(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        return self.dao.delete_by_id(model)

    def delete_all(self, models: List[M]):
        """
        批量根据模型删除数据
        """
        return self.dao.delete_all(models)

    def exists(self, model: M) -> bool:
        """
        根据模型查询判断数据是否存在
        """
        return self.dao.exists(model)

    def count(self, model: M) -> int:
        """
        根据模型统计数据条数
        """
        return self.dao.count(model)

    def find_by_id(self, model: M) -> M:
        """
        根据模型查询指定ID数据
        """
        return self.dao.find_by_id(model)

    def find_by_ids(self, ids: List[int], model: M = None) -> List[M]:
        """
        根据模型查询指定ID数据
        """
        return self.dao.find_by_ids(ids, model)

    def find_all(self, model: M, order: Order = None) -> List[M]:
        """
        根据模型查询所有数据
        """
        return self.dao.find_all(model, order)

    def find_by(self, search: PageHelper[M]) -> Paginate:
        """
        根据模型查询分页数据
        """
        return self.dao.find_by(search)
