# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
应用返回码枚举类
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   CodeEnumpy
@Contact :   sp_hrz@qqcom

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/7/12 12:55   shenpeng   10         None
"""
from enum import Enum


class CodeEnum(Enum):
    # HTTP 状态码
    SUCCESS = {"code": 200, "msg": "成功"}
    BAD_REQUEST = {"code": 400, "msg": "请求错误"}
    UNAUTHORIZED = {"code": 401, "msg": "未授权"}
    FORBIDDEN = {"code": 403, "msg": "禁止访问"}
    NOT_FOUND = {"code": 404, "msg": "没有找到相关信息"}
    INTERNAL_SERVER_ERROR = {"code": 500, "msg": "发生内部错误"}

    # 登录相关
    LOGIN_ERR_PWD = {"code": 400, "msg": "账号或密码错误"}
    LOGIN_TIMEOUT = {"code": 408, "msg": "登录超时"}
    ERROR_TOKEN = {"code": 401, "msg": "无效的token"}
    OTHER_LOGIN = {"code": 401, "msg": "该账号已在其他设备登录"}
    ERR_PERMISSION = {"code": 403, "msg": "权限不足"}

    # 数据库相关
    DB_ERROR = {"code": 500, "msg": "数据库操作失败"}
    DUPLICATE_KEY_ERROR = {"code": 400, "msg": "数据已存在"}
    NO_ROWS_UPDATED = {"code": 500, "msg": "未更新任何数据"}
    NO_ROWS_DELETED = {"code": 500, "msg": "未删除任何数据"}
    ID_NOT_FOUND = {"code": 404, "msg": "数据不存在"}

    # 参数验证相关
    NOT_NULL = {"code": 400, "msg": "参数不能为空"}
    NO_PARAMETER = {"code": 400, "msg": "缺少参数"}
    PARAMETER_ERROR = {"code": 400, "msg": "参数错误"}

    # 文件上传相关
    FILE_NOT_FOUND = {"code": 404, "msg": "文件不存在"}
    ERROR_FILE_TYPE = {"code": 400, "msg": "无效的文件类型"}
    OVER_SIZE = {"code": 400, "msg": "文件大小超出限制"}
    UPLOAD_FAILED = {"code": 500, "msg": "上传失败"}

    # 其他

