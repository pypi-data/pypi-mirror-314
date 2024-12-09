# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
统一异常类定义
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   GlobalExceptionType.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/2 17:30   shenpeng   1.0         None
"""
from xinhou_openai_framework.core.exception.CodeEnum import CodeEnum
from xinhou_openai_framework.core.exception.GlobalBusinessException import GlobalBusinessException


class ServerError(GlobalBusinessException):
    code = CodeEnum.INTERNAL_SERVER_ERROR.value['code']
    msg = CodeEnum.INTERNAL_SERVER_ERROR.value['msg']


class ParameterException(GlobalBusinessException):
    code = CodeEnum.PARAMETER_ERROR.value['code']
    msg = CodeEnum.PARAMETER_ERROR.value['msg']


class LoginFailed(GlobalBusinessException):
    code = CodeEnum.LOGIN_ERR_PWD.value['code']
    msg = CodeEnum.LOGIN_ERR_PWD.value['msg']


class AuthFailed(GlobalBusinessException):
    code = CodeEnum.ERR_PERMISSION.value['code']
    msg = CodeEnum.ERR_PERMISSION.value['msg']


