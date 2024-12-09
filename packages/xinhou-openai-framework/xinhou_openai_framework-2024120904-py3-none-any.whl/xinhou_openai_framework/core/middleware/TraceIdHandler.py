# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
初始化全局TraceID中间件
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   TraceIdMiddlewareHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/20 17:45   shenpeng   1.0         None
"""
import time
import uuid

from fastapi import Request
from starlette.middleware.trustedhost import TrustedHostMiddleware


class TraceIdHandler:

    @staticmethod
    def init_http_filter(app, context):
        # 自定义中间件来生成和处理 TraceID

        @app.middleware("http")
        async def add_trace_id(request: Request, call_next):
            # 从请求头中获取 TraceID，如果不存在则生成一个新的 TraceID
            trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
            # 将 TraceID 添加到请求头中，以便在日志和调用链中使用
            request.state.trace_id = trace_id
            # 继续处理请求
            response = await call_next(request)
            # 添加 TraceID 到响应头中
            response.headers["X-Trace-ID"] = trace_id
            return response

        # 注册中间件
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
        app.middleware("http")(add_trace_id)


