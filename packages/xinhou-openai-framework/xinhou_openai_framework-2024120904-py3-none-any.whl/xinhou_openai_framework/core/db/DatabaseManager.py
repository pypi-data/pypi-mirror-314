# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
数据库管理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   DatabaseManager.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/20 16:34   shenpeng   1.0         None
"""
from loguru import logger
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from xinhou_openai_framework.core.orm.tools.SQLAlchemyInterceptor import intercept_sql_execution

Base = declarative_base()


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def connect(self, context):
        db_url_list = context.framework.datasource.url.split("//")
        db_url = "{0}//{1}:{2}@{3}".format(db_url_list[0], context.framework.datasource.username,
                                           context.framework.datasource.password, db_url_list[1])

        pool_size = context.framework.datasource.pool.pool_size
        pool_pre_ping = context.framework.datasource.pool.pool_pre_ping
        pool_timeout = context.framework.datasource.pool.pool_timeout

        try:
            self.engine = create_engine(
                db_url,
                poolclass=QueuePool,
                pool_size=pool_size,
                pool_pre_ping=pool_pre_ping,
                pool_timeout=pool_timeout,  # 连接池没有线程最多等待时间
                pool_recycle=3600,  # 多久之后对连接池中的线程进行一次连接回收（重置）
                max_overflow=5,  # 超过连接池大小外最多创建连接数
                connect_args={"connect_timeout": 60},
                echo=context.framework.datasource.pool.echo,
                echo_pool=True
            )
        except exc.SQLAlchemyError as e:
            # 处理连接错误
            logger.error(f"Failed to connect to the database: {e}")
            return

        self.SessionLocal = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )

    def disconnect(self):
        if self.engine is not None:
            try:
                self.SessionLocal.remove()  # 移除线程本地会话
                self.engine.dispose()
            except exc.SQLAlchemyError as e:
                # 处理断开连接错误
                logger.error(f"Failed to disconnect from the database: {e}")

            self.engine = None
            self.SessionLocal = None

    def get_session(self):
        session = self.SessionLocal()
        try:
            # intercept_sql_execution(session)
            yield session
            session.commit()  # 提交在上下文中的更改
        except Exception:
            session.rollback()  # 如果出现异常，则回滚更改
            raise
        finally:
            session.close()  # 在使用后关闭会话

    def query(self, *entities, session=None, **kwargs):
        session = session or self.get_session()
        return session.query(*entities, **kwargs)

    def add(self, entity, session=None):
        session = session or self.get_session()
        session.add(entity)

    def delete(self, entity, session=None):
        session = session or self.get_session()
        session.delete(entity)

    def commit(self, session=None):
        session = session or self.get_session()
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            # 处理提交错误
            session.rollback()
            logger.error(f"Failed to commit changes to the database: {e}")

    def rollback(self, session=None):
        session = session or self.get_session()
        session.rollback()

    def refresh(self, entity, session=None):
        session = session or self.get_session()
        session.refresh(entity)


if __name__ == '__main__':
    # # 创建 DatabaseManager 实例
    # database_manager = DatabaseManager.get_instance()
    #
    # # 连接数据库
    # context = AppContext()  # 假设已经创建了合适的 AppContext 对象
    # database_manager.connect(context)
    #
    # # 获取会话对象
    # session = database_manager.get_session()
    #
    # # 执行查询
    # result = database_manager.query(User).filter(User.id == 1).first()
    # logger.info(result)
    #
    # # 添加实体对象
    # user = User(name="John")
    # database_manager.add(user)
    #
    # # 提交事务
    # database_manager.commit()
    #
    # # 断开数据库连接
    # database_manager.disconnect()

    pass
