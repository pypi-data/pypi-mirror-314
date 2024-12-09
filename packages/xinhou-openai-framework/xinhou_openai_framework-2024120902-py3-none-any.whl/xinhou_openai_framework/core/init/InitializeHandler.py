# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局应用初始化代理类
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   InitializeHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 13:43   shenpeng   1.0         None
"""
import logging

from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.logger.Logger import Logger

logger = Logger("InitializeHandler", logging.DEBUG)


class InitializeHandler:
    """
    应用初始化处理类
    """

    @staticmethod
    def init_event(app, context: AppContext):
        @app.on_event("startup")
        async def startup_print_banner():
            # ANSI 转义序列用于设置控制台输出的颜色
            GREEN = "\033[1;32m"
            RESET = "\033[0m"

            # 这里是您提供的 Banner 信息
            banner_info = {
                "name": context.application.name,
                "version": context.application.version,
                "author": context.application.author,
                "email": context.application.email,
                "active_env": context.framework.profiles.active,
            }

            # 定义启动 Banner 的格式，并设置为绿色
            banner = f"""{GREEN}
=========================Welcome to {{name}} !============================
Application:      {{name}}
Version:          {{version}}
Author:           {{author}}
Email:            {{email}}
DEPLOY_ENV:       {{active_env}}
========================================= End =========================================={RESET}"""
            logger.info(banner.format(**banner_info))
