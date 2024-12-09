# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   AppContents.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 14:30   shenpeng   1.0         None
"""
import os


class AppContents:
    # 全局常量

    DEPLOY_ENV = 'DEPLOY_ENV'

    # 上下文常量
    CTX_CONFIG_FILE = "application.yml"
    CTX_YML_NODE_CLOUD = 'cloud'

    CTX_NACOS_MANAGER = 'NacosManager'
    CTX_NACOS_BEAT_INTERVAL_KEY = 'beat_interval'
    CTX_NACOS_BEAT_INTERVAL_DEFAULT_VALUE = 60

    CTX_SKYWALKING_KEY = 'skywalking'

    CTX_INIT_LOGS_DIR = 'logs'

    # 路由常量
    CTX_ROUTER_API_NAME = "api"
    CTX_ROUTER_CONTROLLER = "Controller.py"
    CTX_ROUTER_SOCKET = "Socket.py"
    CTX_ROUTER_APPS_DIR = "apps"
    CTX_ROUTER_FILE_EXTENSION = ".py"
    CTX_ROUTER_POINT = "."

    def CTX_ENV_CONFIG_FILE(run_env):
        return f"application-{run_env}.yml"
