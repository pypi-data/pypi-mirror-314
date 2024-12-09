# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Nacos服务调用功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   NacosHttpClientInvoker.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/10 14:19   shenpeng   1.0         None
"""

from functools import wraps
from typing import Callable

import requests
from loguru import logger
from retry import retry

from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.context.model.SystemContext import ctx


class NacosHttpClientInvoker:
    """
    Nacos 服务调用器，用于调用注册在 Nacos 服务注册中心的服务。
    """

    def __init__(self, server_addr, username, password, namespace_id, group):
        """
        初始化 Nacos 服务调用器

        Args:
            server_addr (str): Nacos 服务器地址，格式为 "host:port"
            username (str): Nacos 登录用户名
            password (str): Nacos 登录密码
            namespace_id (str): Nacos 命名空间 ID
            group (str): Nacos 服务所属的分组
        """
        self.server_addr = server_addr
        self.username = username
        self.password = password
        self.namespace_id = namespace_id
        self.group = group

        # 使用用户名和密码登录 Nacos，获取访问令牌
        response = requests.post(f"http://{self.server_addr}/nacos/v1/auth/login",
                                 params={"username": self.username, "password": self.password})
        body = response.json()
        self.access_token = body["accessToken"]

    @retry(exceptions=requests.exceptions.RequestException, tries=3, delay=1, backoff=2)
    def call_service_http(self, service_name, path="/health", method="GET", headers=None, json_data=None, timeout=5):
        """
        调用注册在 Nacos 服务注册中心的 HTTP 服务

        Args:
            service_name (str): 服务名称
            path (str): 服务路径，默认为 "/health"
            method (str): HTTP 方法，默认为 "GET"
            headers (dict): HTTP 请求头部信息
            json_data (dict): HTTP 请求的 JSON 数据
            timeout (int): 超时时间，默认为 5 秒

        Returns:
            dict: 包含调用结果的字典，格式为 {"code": int, "msg": str, "data": dict}
        """
        try:
            # 获取服务实例列表
            response = requests.get(f"http://{self.server_addr}/nacos/v1/ns/instance/list", params={
                "serviceName": service_name,
                "namespaceId": self.namespace_id,
                "groupName": self.group,
                "healthyOnly": True,
                "accessToken": self.access_token
            })
            response.raise_for_status()  # 检查是否请求成功
            service_instances = response.json()  # 解析服务实例信息
        except Exception as e:
            logger.error(f"获取服务 {service_name} 实例失败：{str(e)}")
            return {"code": response.status_code, "msg": f"获取服务 {service_name} 实例失败", "data": None}

        if not service_instances:
            return {"code": 404, "msg": f"未找到可用的 {service_name} 服务实例", "data": None}

        # 遍历服务实例列表，尝试调用服务
        for instance in service_instances["hosts"]:
            try:
                response = requests.request(method, url=f"http://{instance['ip']}:{instance['port']}{path}",
                                            headers=headers, json=json_data, timeout=30)
                if response.status_code == 200:
                    return {"code": response.status_code, "msg": "调用服务成功", "data": response.json()}
                else:
                    logger.error(f"调用服务 {service_name} 的方法 {method} 失败：HTTP 状态码 {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"调用服务 {service_name} 的方法 {method} 发生错误：{str(e)}")
        return {"code": 500, "msg": f"服务 {service_name} 调用失败，已降级处理", "data": None}


def remote_service(service_name: str = None, path: str = None, method: str = "GET", headers: dict = None,
                   json_data: dict = None, timeout: int = 5):
    """
    远程服务调用装饰器，用于将调用 Nacos 服务的过程封装成一个装饰器。

    Args:
        path (str): 服务路径，默认为 "/health"
        method (str): HTTP 方法，默认为 "GET"
        headers (dict): HTTP 请求头部信息
        json_data (dict): HTTP 请求的 JSON 数据
        timeout (int): 超时时间，默认为 5 秒

    Returns:
        Callable: 装饰器函数
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context: AppContext = ctx.__getattr__("context")  # 获取全局变量
            invoker = NacosHttpClientInvoker(
                server_addr=context.framework.cloud.nacos.discovery.server_addr,
                username=context.framework.cloud.nacos.discovery.username,
                password=context.framework.cloud.nacos.discovery.password,
                namespace_id=context.framework.cloud.nacos.discovery.namespace_id,
                group=context.framework.cloud.nacos.discovery.group
            )

            return func(*args, remote_result=invoker.call_service_http(
                service_name=service_name,
                path=path,
                method=method,
                headers=headers,
                json_data=json_data,
                timeout=timeout
            ), **kwargs)

        return wrapper

    return decorator


class OpenaiAdminRemoteService:
    """
    OpenaiAdmin 远程服务类，用于封装调用 Nacos 服务的方法。
    """

    @remote_service(service_name="xinhou-openai-framework", path="/health", method="GET")
    def get_health(self, remote_result=None):
        """
        获取服务健康状态的方法。

        Args:
            remote_result (dict): 远程调用结果

        Returns:
            dict: 包含调用结果的字典
        """
        if remote_result["code"] == 200:
            return {'code': 200, "msg": "success", "data": remote_result["data"]}
        else:
            return {"code": remote_result["code"], 'msg': "failure", "message": remote_result["msg"]}


if __name__ == "__main__":
    # 示例代码
    server_address = "nacos.xinhouai.com:80"
    username = "xinhou-test"
    password = "aegie9aiG6cu6eeh"
    namespace_id = '89d52cdc-adac-49e8-8c3e-7e132f430e7e'
    group = "XINHOU_OPENAI_GROUP"
    service_name = "xinhou-openai-framework"

    invoker = NacosHttpClientInvoker(server_address, username, password, namespace_id, group)
    result = invoker.call_service_http(service_name)
    print(result)  # 通过Open API 调用服务

    service = OpenaiAdminRemoteService()
    result = service.get_health()  # 通过service注解实现
    print(result)
