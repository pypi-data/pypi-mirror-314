# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局配置初始化管理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   manager.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/14 17:28   shenpeng   1.0         None
"""

import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from xinhou_openai_framework.core.beans.BeansContext import BeansContext
from xinhou_openai_framework.core.cache.CacheHandler import CacheHandler
from xinhou_openai_framework.core.config.ConfigHandler import ConfigHandler
from xinhou_openai_framework.core.contents.AppContents import AppContents
from xinhou_openai_framework.core.context.ContextHandler import ContextHandler
from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.db.DatabaseHandler import DatabaseHandler
from xinhou_openai_framework.core.exception.ExceptionHandler import GlobalExceptionHandler
from xinhou_openai_framework.core.init.InitializeHandler import InitializeHandler
from xinhou_openai_framework.core.logger.LoggerHandler import LoggerHandler
from xinhou_openai_framework.core.middleware.HttpHandler import HttpHandler
from xinhou_openai_framework.core.nacos.NacosHandler import NacosHandler
from xinhou_openai_framework.core.nacos.NacosManager import NacosManager
from xinhou_openai_framework.core.router.RouterHandler import RouterHandler
from xinhou_openai_framework.core.skywalking.SkywalkingHandler import SkywalkingHandler
from xinhou_openai_framework.utils.ObjDictUtil import ObjectDict


def create_app(run_env=None):
    """
    创建FastAPI对象，执行初始化流程
    :param run_env: 运行环境
    :param config_path: 配置文件路径
    :return: 返回FastApi对象
    """
    # 读取基础配置文件
    read_base_stream_config = ConfigHandler.read_yaml(os.path.join(os.getcwd(), AppContents.CTX_CONFIG_FILE))
    base_ctx = ObjectDict.from_dict(read_base_stream_config)

    # 读取环境配置
    if run_env is None:
        if base_ctx.framework.profiles.active:
            run_env = base_ctx.framework.profiles.active
        if os.environ.get(AppContents.DEPLOY_ENV):
            run_env = os.environ.get(AppContents.DEPLOY_ENV)

    # 加载环境配置文件
    read_env_stream_config = ConfigHandler.read_yaml(
        os.path.join(os.getcwd(), AppContents.CTX_ENV_CONFIG_FILE(run_env)))
    base_env_ctx = ObjectDict.from_dict(read_env_stream_config)

    context: AppContext = AppContext()
    context.append_dist(read_base_stream_config)
    context.append_dist(read_env_stream_config)
    if (hasattr(base_env_ctx.framework, AppContents.CTX_YML_NODE_CLOUD)
            and base_env_ctx.framework.cloud.nacos.config.enabled):
        nacos = NacosManager(
            server_endpoint=base_env_ctx.framework.cloud.nacos.config.server_addr,
            namespace_id=base_env_ctx.framework.cloud.nacos.config.namespace_id,
            username=base_env_ctx.framework.cloud.nacos.config.username,
            password=base_env_ctx.framework.cloud.nacos.config.password
        )
        if base_env_ctx.framework.cloud.nacos.config.shared_configs:
            for data_id in base_env_ctx.framework.cloud.nacos.config.shared_configs:
                context.append_dist(ConfigHandler.load_yaml(
                    nacos.load_conf(
                        data_id=data_id,
                        group=base_env_ctx.framework.cloud.nacos.config.group
                    )))
        else:
            context.append_dist(ConfigHandler.load_yaml(
                nacos.load_conf(
                    data_id=AppContents.CTX_ENV_CONFIG_FILE(run_env),
                    group=base_env_ctx.framework.cloud.nacos.config.group
                )))
    else:
        config_path = os.path.join(os.getcwd(), AppContents.CTX_ENV_CONFIG_FILE(run_env))
        context.append_dist(ConfigHandler.read_yaml(config_path))
    context = ObjectDict.from_dict(context.ctx)
    context.framework.profiles.active = run_env
    # 配置FastAPI对象参数并实例化对象
    app = FastAPI(
        title=context.application.name,
        version=context.application.version,
        contact={
            "name": context.application.author,
            "email": context.application.email,
        },
        openapi_url="/api/v1/openapi.json"
    )

    # 配置会话中间件
    app.add_middleware(SessionMiddleware, secret_key="xinhou_openai_framework_secret_key")
    # 配置静态文件
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # 初始化全局配置
    ContextHandler.init_ctx(app, context)
    # 初始化全局日志
    LoggerHandler.init_logs(app, context)
    # 初始化全局数据库
    DatabaseHandler.init_database(app, context)
    # 初始化全局缓存
    CacheHandler.init_cache(app, context)
    # 初始化全局路由
    RouterHandler.init_routes(app, context)
    # 初始化全局Http中间件
    HttpHandler.init_http_filter(app, context)
    # TraceIdMiddlewareHandler.init_http_middleware(app, context)

    # 初始化全局异常
    GlobalExceptionHandler.init_excepts(app, context)
    # 初始化Nacos注册中心&配置中心
    NacosHandler.init_handler(app, context)
    # 初始化Skywalking全局配置
    SkywalkingHandler.init_handler(app, context)

    # 启动初始化事件
    InitializeHandler.init_event(app, context)
    # 启动初始化全局队列监听器
    # QueueListenerHandler.init_listeners(app, context)

    return app
