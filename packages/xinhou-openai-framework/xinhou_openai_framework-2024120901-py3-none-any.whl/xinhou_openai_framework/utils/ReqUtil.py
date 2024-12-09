# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ReqUtil.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 13:22   shenpeng   1.0         None
"""
from typing import List

import requests
from loguru import logger

from xinhou_openai_framework.utils.ObjDictUtil import ObjectDict


class ReqUtil:
    def __init__(self, base_url):
        """
        初始化 ReqUtil 对象

        :param base_url: 基本的 URL，用于构建请求的绝对 URL
        """

        if not base_url.startswith('http://') and not base_url.startswith('https://'):
            base_url = f'http://{base_url}'  # 如果 URL 不以 http:// 或 https:// 开头，则添加 http://

        self.base_url = base_url
        self.headers = {}
        self.convert_underscores = None
        self.timeout = None

    def set_headers(self, headers_list, convert_underscores=True):
        """
        设置请求头

        :param headers_list: 包含多个字典形式的请求头的列表
        :param convert_underscores: 是否将参数键名中的下划线替换为连字符，默认为 False
        :return: ReqUtil 对象，支持链式调用
        """
        self.convert_underscores = convert_underscores

        for header_dict in headers_list:
            for key, value in header_dict.items():
                new_key = key.replace('_', '-') if self.convert_underscores else key
                # 将值转换为字符串类型
                str_value = str(value) if not isinstance(value, (str, bytes)) else value
                self.headers[new_key] = str_value
        return self

    def set_timeout(self, timeout):
        """
        设置请求超时时间

        :param timeout: 请求超时时间（秒）
        :return: ReqUtil 对象，支持链式调用
        """
        self.timeout = timeout
        return self

    def get(self, endpoint, params=None):
        """
        发送 GET 请求

        :param endpoint: 请求的路径
        :param params: 请求的查询参数
        :return: HTTP 响应对象
        """
        url = self.base_url + endpoint
        response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        return response

    def post(self, endpoint, data=None, json=None):
        """
        发送 POST 请求

        :param endpoint: 请求的路径
        :param data: POST 请求的表单数据
        :param json: POST 请求的 JSON 数据
        :return: HTTP 响应对象
        """
        url = self.base_url + endpoint
        response = requests.post(url, data=data, json=json, headers=self.headers, timeout=self.timeout)
        return response

    def put(self, endpoint, data=None, json=None):
        """
        发送 PUT 请求

        :param endpoint: 请求的路径
        :param data: PUT 请求的表单数据
        :param json: PUT 请求的 JSON 数据
        :return: HTTP 响应对象
        """
        url = self.base_url + endpoint
        response = requests.put(url, data=data, json=json, headers=self.headers, timeout=self.timeout)
        return response

    def delete(self, endpoint):
        """
        发送 DELETE 请求

        :param endpoint: 请求的路径
        :return: HTTP 响应对象
        """
        url = self.base_url + endpoint
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        return response


# 示例用法
if __name__ == "__main__":
    response = ReqUtil("http://127.0.0.1:8848").post("/nacos/v1/auth/login", {"username": "nacos", "password": "nacos"})
    response_object = response.json()
    res_obj = ObjectDict.from_dict(response_object)
    logger.info(res_obj)

    # base_url = "http://openai-embedding.xinhou.com"
    # req_util = ReqUtil(base_url)
    #
    # # response = req_util.header("Authorization", "Bearer token").get("/endpoint")
    # headers = [
    #     {"tenant-id": "888888"},
    #     {"classify-type": "role"},
    #     {"classify-id": "888888"},
    #     {"platform-code": "pt"}
    # ]
    #
    # response = req_util.set_headers(headers).post("/tool/index/index", json={
    #     "username": "zhangsan",
    #     "password": "123456"
    # })
    # response_object = response.json()
    #
    # res_obj = ObjectDict.from_dict(response_object)
    # logger.info(res_obj)

    # payload = {"key1": "value1", "key2": "value2"}
    # response = req_util.post("/endpoint", json=payload)
    #
    # payload = {"key1": "updated_value"}
    # response = req_util.put("/endpoint/123", json=payload)
    #
    # response = req_util.delete("/endpoint/123").timeout(10)
