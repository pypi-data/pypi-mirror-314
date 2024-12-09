# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   BusinessException.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/6 11:31   shenpeng   1.0         None
"""
from xinhou_openai_framework.core.exception.CodeEnum import CodeEnum
from xinhou_openai_framework.core.exception.GlobalBusinessException import GlobalBusinessException


class BusinessException(GlobalBusinessException):
    """
    业务异常
    """

    def __init__(self, code_enum: CodeEnum = None):
        if code_enum:
            self.code = code_enum.value['code']
            self.msg = code_enum.value['msg']
        super(GlobalBusinessException, self).__init__(self.code, self.msg, self.error_code)
