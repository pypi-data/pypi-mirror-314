# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局配置初始化管理器
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   AppManager.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2024/03/29 17:28   shenpeng   1.0         None
"""
import gc
import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from xinhou_openai_framework.core.cache.CacheHandler import CacheHandler
from xinhou_openai_framework.core.config.ConfigHandler import ConfigHandler
from xinhou_openai_framework.core.contents.AppContents import AppContents
from xinhou_openai_framework.core.context.ContextHandler import ContextHandler
from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.db.DatabaseHandler import DatabaseHandler
from xinhou_openai_framework.core.exception.ExceptionHandler import GlobalExceptionHandler
from xinhou_openai_framework.core.init.InitializeHandler import InitializeHandler
from xinhou_openai_framework.core.logger.LoggerHandler import LoggerHandler
from xinhou_openai_framework.core.logger.LoggingManager import LoggingManager
from xinhou_openai_framework.core.middleware.HttpHandler import HttpHandler
from xinhou_openai_framework.core.nacos.NacosHandler import NacosHandler
from xinhou_openai_framework.core.nacos.NacosManager import NacosManager
from xinhou_openai_framework.core.router.RouterHandler import RouterHandler
from xinhou_openai_framework.core.skywalking.SkywalkingHandler import SkywalkingHandler
from xinhou_openai_framework.utils.ObjDictUtil import ObjectDict


class AppManager:
    @classmethod
    def create_app(cls, run_env=None):
        """
        创建FastAPI对象，执行初始化流程
        :param run_env: 运行环境
        :return: 返回FastApi对象
        """
        LoggingManager.init_before_logger(os.path.join(os.getcwd(), AppContents.CTX_INIT_LOGS_DIR))
        base_ctx, base_env_ctx = cls.load_configs(run_env)
        context = cls.setup_context(base_ctx, base_env_ctx)
        app = cls.configure_fastapi_app(context)
        cls.setup_global_components(app, context)
        cls.start_initialization_events(app, context)
        return app

    @staticmethod
    def load_configs(run_env):
        # 加载基础配置
        read_base_stream_config = ConfigHandler.read_yaml(os.path.join(os.getcwd(), AppContents.CTX_CONFIG_FILE))
        base_ctx = ObjectDict.from_dict(read_base_stream_config)

        # 加载环境配置
        if run_env is None:
            run_env = os.environ.get(AppContents.DEPLOY_ENV) or base_ctx.framework.profiles.active
            base_ctx.framework.profiles.active = run_env
        read_env_stream_config = ConfigHandler.read_yaml(
            os.path.join(os.getcwd(), AppContents.CTX_ENV_CONFIG_FILE(run_env)))
        base_env_ctx = ObjectDict.from_dict(read_env_stream_config)
        return base_ctx, base_env_ctx

    @staticmethod
    def setup_context(base_ctx, base_env_ctx):
        context: AppContext = AppContext()
        context.append_dist(base_ctx)
        context.append_dist(base_env_ctx)
        if (hasattr(base_env_ctx.framework, AppContents.CTX_YML_NODE_CLOUD)
                and base_env_ctx.framework.cloud.nacos.config.enabled):
            context = AppManager.load_nacos_configs(context, base_env_ctx)
        else:
            config_path = os.path.join(os.getcwd(), AppContents.CTX_ENV_CONFIG_FILE(base_ctx.framework.profiles.active))
            context.append_dist(ConfigHandler.read_yaml(config_path))
        return ObjectDict.from_dict(context.ctx)

    @staticmethod
    def load_nacos_configs(context, base_env_ctx):
        # 加载Nacos配置
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
                    data_id=AppContents.CTX_ENV_CONFIG_FILE(base_env_ctx.framework.profiles.active),
                    group=base_env_ctx.framework.cloud.nacos.config.group
                )))
        return context

    @staticmethod
    def configure_fastapi_app(context):
        # 配置FastAPI对象参数并实例化对象
        gc.set_threshold(700, 10, 10)
        gc.enable()
        app = FastAPI(
            title=context.application.name,
            version=context.application.version,
            contact={
                "name": context.application.author,
                "email": context.application.email,
            },
            openapi_url="/api/v1/openapi.json"
        )
        app.add_middleware(SessionMiddleware, secret_key="xinhou_openai_framework_secret_key")
        app.mount("/static", StaticFiles(directory="static"), name="static")
        return app

    @staticmethod
    def setup_global_components(app, context):
        # 初始化全局配置、路由、Http中间件、异常处理、数据库、缓存、Nacos、Skywalking、日志
        ContextHandler.init_ctx(app, context)
        RouterHandler.init_routes(app, context)
        GlobalExceptionHandler.init_excepts(app, context)
        DatabaseHandler.init_database(app, context)
        CacheHandler.init_cache(app, context)
        HttpHandler.init_http_filter(app, context)
        NacosHandler.init_handler(app, context)
        SkywalkingHandler.init_handler(app, context)
        LoggerHandler.init_logs(app, context)

    @staticmethod
    def start_initialization_events(app, context):
        # 启动初始化事件
        InitializeHandler.init_event(app, context)
