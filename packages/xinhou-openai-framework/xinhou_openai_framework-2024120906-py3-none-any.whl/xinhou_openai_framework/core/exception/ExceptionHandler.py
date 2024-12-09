# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
初始化全局异常代理文件
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ExceptionHandler.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/7/12 12:55   shenpeng   1.0         None
"""
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.exception.CodeEnum import CodeEnum
from xinhou_openai_framework.core.exception.GlobalBusinessException import GlobalBusinessException
from xinhou_openai_framework.core.reponse.R import R


class GlobalExceptionHandler:
    """
    全局异常处理
    """

    @staticmethod
    def init_excepts(app, context: AppContext):
        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            message = []
            for error in exc.errors():
                message.append({"field": ".".join(error.get("loc")), "cause": error.get("msg")})
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"code": CodeEnum.PARAMETER_ERROR.value['code'], "msg": CodeEnum.PARAMETER_ERROR.value['msg'],
                         "data": message}
            )

        @app.exception_handler(Exception)
        async def exception_handler(req: Request, e: Exception):
            """全局处理错误方法"""
            logger.error(e)  # 对错误进行日志记录

            if isinstance(e, GlobalBusinessException):
                # 处理 GlobalBusinessException 异常并返回其自定义消息体
                return JSONResponse(e.get_body())

            if isinstance(e, HTTPException):
                # 处理 FastAPI 内置的 HTTPException 并返回 R.REQUEST_ERROR
                return R.REQUEST_ERROR()

            if isinstance(e, FileNotFoundError):
                # 处理 FileNotFoundError 异常并返回 R.FILE_NO_FOUND
                return R.FILE_NO_FOUND()

            # 默认情况下，返回 R.SERVER_ERROR
            return R.SERVER_ERROR()
