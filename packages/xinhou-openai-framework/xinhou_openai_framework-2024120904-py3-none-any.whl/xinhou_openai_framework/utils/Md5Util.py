# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   Md5Util.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/3/27 21:44   shenpeng   1.0         None
"""

import hashlib


class Md5Util:
    """计算MD5的工具类"""

    @staticmethod
    def md5_string(s: str) -> str:
        """计算字符串的MD5摘要"""
        md5 = hashlib.md5()
        md5.update(s.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def md5_file(file_path: str) -> str:
        """计算文件的MD5摘要"""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()
