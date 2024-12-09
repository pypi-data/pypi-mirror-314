# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局路由初始化处理类

自动注册路由规则：
1、控制器的命名规则 TestController.py  业务名称+Controller
2、控制器内部 路由命名 api = APIRouter()
    a.路由变量统一使用api变量名
    b.路由名称 模块+类名(或文件名) ：'home:docker'
    c.路由前缀（必须添加）
    d.路由注解 统一使用 @api.route('/index')
3、路由扫描时根据 扫描指定项目(xinhou-openai-framework)下的 应用层(apps) 的所有目录下的Controller文件
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   RouterHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/7/13 17:11   shenpeng   1.0         None
"""
import importlib
import os

from xinhou_openai_framework.core.common.controller.CommonController import base_common_api
from xinhou_openai_framework.core.common.controller.GenerateCodeController import code_generater_api
from xinhou_openai_framework.core.contents.AppContents import AppContents
from xinhou_openai_framework.utils.PathUtil import PathUtil
from xinhou_openai_framework.utils.StrUtil import StrUtil


class RouterHandler:
    """
    全局路由初始化处理类

    自动注册路由规则：
    1、控制器的命名规则 IndexController.py  业务名称+Controller,已支持 Controller 和 Socket
    2、控制器内部 路由命名 api = APIRouter()
        a.路由变量统一使用api变量名
        b.路由名称 模块+类名(或文件名) ：'home:docker'
        c.路由前缀（必须添加）
        d.路由注解 统一使用 @api.route('/index')
    3、路由扫描时根据 扫描指定项目(xinhou-openai-framework)下的 应用层(apps) 的所有目录下的Controller文件
    """

    @staticmethod
    def init_routes(app, context):
        """
        自动扫描 初始化 应用路由路由
        :param app:
        :return:
        """
        # 循环注册路由
        for router in [
            base_common_api,
            code_generater_api,
        ]:
            app.include_router(router)
        RouterHandler.auto_scan_routes(app,
                                       PathUtil.get_root_path() + os.sep + AppContents.CTX_ROUTER_APPS_DIR)  # 自动扫描路由

    @staticmethod
    def auto_scan_routes(app, filePath):
        """
        自动扫描路由注册
        :param app:
        :param filePath:
        :return:
        """
        file_list = os.listdir(filePath)
        for file_name in file_list:  # 循环文件&文件夹类别
            if os.path.isdir(os.path.join(filePath, file_name)):
                RouterHandler.auto_scan_routes(app, os.path.join(filePath, file_name))
            else:
                if file_name.find(AppContents.CTX_ROUTER_CONTROLLER) > -1 or file_name.find(
                        AppContents.CTX_ROUTER_SOCKET) > -1:
                    clazz_path = StrUtil.sub_str_after(filePath, AppContents.CTX_ROUTER_APPS_DIR).replace(os.sep,
                                                                                                          AppContents.CTX_ROUTER_POINT)
                    clazz_name = StrUtil.sub_str_before(file_name, AppContents.CTX_ROUTER_FILE_EXTENSION)
                    clazz_full = clazz_path + AppContents.CTX_ROUTER_POINT + clazz_name
                    auto_route_module_controller_class = importlib.import_module(clazz_full)
                    flag = AppContents.CTX_ROUTER_API_NAME in auto_route_module_controller_class.__dict__
                    if flag:
                        module_controller_route_class = auto_route_module_controller_class.__dict__[
                            AppContents.CTX_ROUTER_API_NAME]
                        app.include_router(module_controller_route_class)  # 注册路由
                        # logger.info(" * auto scan route name：", clazz_full)
