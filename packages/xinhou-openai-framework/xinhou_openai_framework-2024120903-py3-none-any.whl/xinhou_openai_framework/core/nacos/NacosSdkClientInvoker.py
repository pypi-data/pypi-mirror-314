# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Nacos服务调用功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   NacosSdkClientInvoker.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/10 14:19   shenpeng   1.0         None
"""
from loguru import logger
from functools import wraps
from typing import Callable

import requests
from nacos.client import NacosClient
from retry import retry

from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.context.model.SystemContext import ctx


class NacosSdkClientInvoker:
    def __init__(self, server_addr, username, password, namespace_id, group):
        """
        初始化 Nacos 服务调用器

        Args:
            server_addr (str): Nacos 服务器地址，格式为 "host:port"
            namespace_id (str): Nacos 命名空间 ID
            group (str): Nacos 服务所属的分组
        """
        self.client = NacosClient(
            server_addresses=server_addr,
            username=username,
            password=password,
            namespace=namespace_id
        )
        self.server_addr = server_addr
        self.namespace_id = namespace_id
        self.group = group
        response = requests.post(f"http://{self.server_addr}/nacos/v1/auth/login",
                                 params={"username": username, "password": password})
        body = response.json()
        self.access_token = body["accessToken"]

    @retry(exceptions=requests.exceptions.RequestException, tries=3, delay=1, backoff=2)
    def call_service_client(self, service_name, method="GET", path="/health", headers=None, json_data=None, timeout=15):
        """
        调用指定服务的方法

        Args:
            service_name (str): 要调用的服务名称
            method (str): HTTP 方法，默认为 "GET"
            path (str): 路径，默认为 "/health"
            headers (dict): HTTP 请求头，默认为 None
            json_data (dict): 请求数据，默认为 None
            timeout (int): 超时时间，默认为 5 秒

        Returns:
            dict: 包含调用结果的字典，包括 code、msg 和 data 三个字段
        """
        try:
            service_instances = self.client.list_naming_instance(
                service_name=service_name,
                namespace_id=self.namespace_id,
                group_name=self.group,
                healthy_only=True)
        except Exception as e:
            logger.error(f"获取服务 {service_name} 实例失败：{str(e)}")
            return {"code": 404, "msg": f"获取服务 {service_name} 实例失败", "data": None}

        if not service_instances:
            return {"code": 404, "msg": f"未找到可用的 {service_name} 服务实例", "data": None}

        for instance in service_instances['hosts']:
            try:
                response = requests.request(method, f"http://{instance['ip']}:{instance['port']}{path}",
                                            headers=headers, json=json_data, timeout=timeout)
                if response.status_code == 200:
                    return {"code": response.status_code, "msg": "调用服务成功", "data": response.json()}
                else:
                    logger.error(f"调用服务 {service_name} 的方法 {method} 失败：HTTP 状态码 {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"调用服务 {service_name} 的方法 {method} 发生错误：{str(e)}")

        return {"code": 500, "msg": f"服务 {service_name} 调用失败，已降级处理", "data": None}


def remote_service(service_name: str = None, path: str = "/health", method: str = "GET", headers: dict = None,
                   json_data: dict = None, timeout: int = 5):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context: AppContext = ctx.__getattr__("context")  # 全局变量
            invoker = NacosSdkClientInvoker(
                server_addr=context.framework.cloud.nacos.discovery.server_addr,
                username=context.framework.cloud.nacos.discovery.username,
                password=context.framework.cloud.nacos.discovery.password,
                namespace_id=context.framework.cloud.nacos.discovery.namespace_id,
                group=context.framework.cloud.nacos.discovery.group
            )

            return func(*args, remote_result=invoker.call_service_client(
                service_name=service_name,
                path=path,
                method=method,
                headers=headers,
                json_data=json_data,
                timeout=timeout
            ), **kwargs)

        return wrapper

    return decorator


class RemoteService:
    @remote_service(service_name="xinhou-openai-framework", path="/health", method="GET")
    def get_health(self, remote_result=None):
        if remote_result["code"] == 200:
            return {'code': 200, "msg": "success", "data": remote_result["data"]}
        else:
            return {"code": remote_result["code"], 'msg': "failure", "message": remote_result["msg"]}


def main():
    # server_address = "nacos.xinhouai.com:80"
    # username = "nacos"
    # password = "nacos"
    # namespace_id = '89d52cdc-adac-49e8-8c3e-7e132f430e7e'
    # group = "XINHOU_OPENAI_GROUP"
    # service_name = "xinhou-openai-framework"
    #
    # invoker = NacosInvoker(server_address, username, password, namespace_id, group)
    # result = invoker.call_service_http(service_name)
    # print(result)  # 通过Open API 调用服务
    #
    # result2 = invoker.call_service_client(service_name)
    # print(result2)  # 通过客户端调用服务

    service = RemoteService()
    result = service.get_health()
    print(result)


if __name__ == "__main__":
    main()
