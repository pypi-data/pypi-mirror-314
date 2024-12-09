# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
初始化数据库处理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   DatabaseHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/3 15:00   shenpeng   1.0         None
"""
from xinhou_openai_framework.core.db.DatabaseManager import DatabaseManager


class DatabaseHandler:
    @staticmethod
    def init_database(app, context):
        @app.on_event("startup")
        async def startup_database_manager_event():
            # 初始化数据库连接和管理器
            db_manager = DatabaseManager.get_instance()
            db_manager.connect(context)

        @app.on_event("shutdown")
        async def shutdown_database_manager_event():
            # 关闭数据库连接和管理器
            db_manager = DatabaseManager.get_instance()
            db_manager.disconnect()
