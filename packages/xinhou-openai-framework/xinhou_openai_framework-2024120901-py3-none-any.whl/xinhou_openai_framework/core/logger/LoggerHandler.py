# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局日志初始化代理类
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   LoggerHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/18 18:37   shenpeng   1.0         None
"""
import logging
import os

from xinhou_openai_framework.core.contents.AppContents import AppContents
from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.logger.LoggerManager import LoggerManager
from xinhou_openai_framework.core.logger.LoggingManager import LoggingManager


class LoggerHandler:
    """
    日志处理类
    """

    @staticmethod
    def init_logs(app, context: AppContext):
        @app.on_event("startup")
        async def startup_logger_manager_event():
            if context.framework.logging.path is None:
                LoggingManager.init_logger(app, os.path.join(os.getcwd(), AppContents.CTX_INIT_LOGS_DIR))
            else:
                LoggingManager.init_logger(app, os.path.join(os.getcwd(), context.framework.logging.path))
