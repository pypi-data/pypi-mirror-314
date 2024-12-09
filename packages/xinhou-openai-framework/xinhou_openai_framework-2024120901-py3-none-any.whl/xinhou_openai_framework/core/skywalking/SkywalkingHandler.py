# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
初始化缓存处理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   CacheHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/4/4 17:33   shenpeng   1.0         None
"""

from skywalking import agent, config

from xinhou_openai_framework.core.contents.AppContents import AppContents
from xinhou_openai_framework.core.context.model.AppContext import AppContext


class SkywalkingHandler:

    @staticmethod
    def init_handler(app, context: AppContext):
        @app.on_event("startup")
        def startup_skywalking_manager_event():
            if (hasattr(context.framework, AppContents.CTX_SKYWALKING_KEY)):
                if context.framework.skywalking.enable:
                    # 初始化 SkyWalking
                    config.init(
                        agent_collector_backend_services=context.framework.skywalking.agent_collector_backend_services,
                        agent_name=context.framework.skywalking.agent_name,
                        agent_instance_name=context.framework.skywalking.agent_instance_name,
                        agent_namespace=context.framework.skywalking.agent_namespace
                    )

                    # 启动 SkyWalking Agent
                    agent.start()