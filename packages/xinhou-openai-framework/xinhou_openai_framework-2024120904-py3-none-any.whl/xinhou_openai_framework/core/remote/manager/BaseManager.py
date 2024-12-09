# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   BaseManagerImpl.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/6 10:47   shenpeng   1.0         None
"""
from typing import TypeVar, Generic, List, Optional
from loguru import logger
from pydantic import BaseModel

from xinhou_openai_framework.core.exception.GlobalBusinessException import GlobalBusinessException
from xinhou_openai_framework.utils.ObjDictUtil import ObjectDict
from xinhou_openai_framework.utils.ReqUtil import ReqUtil

M = TypeVar('M', bound=BaseModel)


class BaseManagerImpl(Generic[M]):
    """
    远程调用基础Manager管理类
    """

    def request_tool(self, service_url: str, url: str, headers: Optional[List[dict]] = None,
                     body: Optional[dict] = None) -> ObjectDict:
        """
        发送POST请求到指定的服务端点，并处理返回结果。

        Args:
        - service_url (str): 服务的URL地址
        - url (str): 要发送POST请求的端点URL
        - headers (Optional[dict]): 请求头信息，默认为None
        - body (Optional[dict]): POST请求的JSON数据，默认为None

        Returns:
        - dict: 处理后的返回结果(只返回数据结果)

        Raises:
        - GlobalBusinessException: 如果状态码不是200，则引发全局业务异常
        """

        req_util = ReqUtil(service_url)
        logger.info(f"service_url:{service_url}")
        logger.info("service_headers:{}".format(headers))
        logger.info("service_body:{}".format(body))
        response = req_util.set_headers(headers).post(url, json=body)
        if response.status_code == 200: # http级别
            response_object = response.json()
            logger.info("service_response:{}".format(response_object))
            res_obj = ObjectDict.from_dict(response_object)
            if res_obj.code == 200: # 接口层级
                return res_obj.data
            else:
                raise GlobalBusinessException(res_obj.code, res_obj.msg)
        else:
            raise GlobalBusinessException(response.status_code, response.reason)
