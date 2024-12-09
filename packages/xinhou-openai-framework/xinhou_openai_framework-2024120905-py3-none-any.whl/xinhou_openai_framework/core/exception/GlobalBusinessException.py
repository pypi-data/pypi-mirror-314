# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   marmot-xinhou-openai-framework  
@File    :   GlobalBusinessException.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/2 17:31   shenpeng   1.0         None
"""


class GlobalBusinessException(Exception):
    """
    全局异常
    """

    code = 500
    msg = '系统发生异常请稍后再试.'

    def __init__(self, code=None, msg=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        super(GlobalBusinessException, self).__init__(self.code, self.msg)

    def get_body(self):
        return {"code": self.code, "msg": self.msg}
