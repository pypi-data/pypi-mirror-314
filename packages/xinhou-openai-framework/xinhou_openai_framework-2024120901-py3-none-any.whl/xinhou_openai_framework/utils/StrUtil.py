# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   StrUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/17 14:08   shenpeng   1.0         None
"""
import re
import time
from typing import List

from loguru import logger


class StrUtil:
    @staticmethod
    def is_empty(s):
        """
        判断字符串是否为空
        :param s: 字符串
        :return: True or False
        """
        return s is None or len(s.strip()) == 0

    @staticmethod
    def is_not_empty(s):
        """
        判断字符串是否不为空
        :param s: 字符串
        :return: True or False
        """
        return not StrUtil.is_empty(s)

    @staticmethod
    def is_blank(s):
        """
        判断字符串是否为空白字符串
        :param s: 字符串
        :return: True or False
        """
        return s is None or len(s.strip()) == 0

    @staticmethod
    def is_not_blank(s):
        """
        判断字符串是否不为空白字符串
        :param s: 字符串
        :return: True or False
        """
        return not StrUtil.is_blank(s)

    @staticmethod
    def equals(s1, s2):
        """
        判断两个字符串是否相等
        :param s1: 字符串1
        :param s2: 字符串2
        :return: True or False
        """
        return s1 == s2

    @staticmethod
    def equals_ignore_case(s1, s2):
        """
        判断两个字符串是否相等（忽略大小写）
        :param s1: 字符串1
        :param s2: 字符串2
        :return: True or False
        """
        return s1.lower() == s2.lower()

    @staticmethod
    def contains(s, sub):
        """
        判断字符串是否包含子串
        :param s: 字符串
        :param sub: 子串
        :return: True or False
        """
        return sub in s

    @staticmethod
    def starts_with(s, prefix):
        """
        判断字符串是否以指定前缀开头
        :param s: 字符串
        :param prefix: 前缀
        :return: True or False
        """
        return s.startswith(prefix)

    @staticmethod
    def ends_with(s, suffix):
        """
        判断字符串是否以指定后缀结尾
        :param s: 字符串
        :param suffix: 后缀
        :return: True or False
        """
        return s.endswith(suffix)

    @staticmethod
    def substring(s, start, end=None):
        """
        截取字符串
        :param s: 字符串
        :param start: 起始位置
        :param end: 结束位置（可选）
        :return: 截取后的字符串
        """
        return s[start:end]

    @staticmethod
    def replace(s, old, new):
        """
        替换字符串中的子串
        :param s: 字符串
        :param old: 要替换的子串
        :param new: 替换后的子串
        :return: 替换后的字符串
        """
        return s.replace(old, new)

    @staticmethod
    def to_lower_case(s):
        """
        将字符串转换为小写
        :param s: 字符串
        :return: 转换后的字符串
        """
        return s.lower()

    @staticmethod
    def to_upper_case(s):
        """
        将字符串转换为大写
        :param s: 字符串
        :return: 转换后的字符串
        """
        return s.upper()

    @staticmethod
    def trim(s):
        """
        去除字符串两端的空格
        :param s: 字符串
        :return: 去除空格后的字符串
        """
        return s.strip()

    @staticmethod
    def join(iterable, separator):
        """
        将可迭代对象中的元素用指定分隔符连接成一个字符串
        :param iterable: 可迭代对象
        :param separator: 分隔符
        :return: 连接后的字符串
        """
        return separator.join(iterable)

    @staticmethod
    def index(s: str, sub: str) -> int:
        return s.index(sub)

    @staticmethod
    def find(s: str, sub: str) -> int:
        return s.find(sub)

    @staticmethod
    def find_is_exists(s: str, sub: str) -> bool:
        return s.find(sub) != -1

    @staticmethod
    def sub_str_before(s: str, sub: str) -> str:
        return s[0:s.find(sub)]

    @staticmethod
    def sub_str_after(s: str, sub: str, contain: bool = False) -> str:
        if contain:
            return s[s.rfind(sub) + len(sub):]
        else:
            return s[s.rfind(sub):]

    @staticmethod
    def split(s: str, sub: str = "") -> List[str]:
        return s.split(sub)

    @staticmethod
    def to_camel_case(x):
        """转驼峰法命名"""
        return re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x)

    @staticmethod
    def to_upper_camel_case(x):
        """转大驼峰法命名"""
        s = re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x)
        return s[0].upper() + s[1:]

    @staticmethod
    def to_lower_camel_case(x):
        """转小驼峰法命名"""
        s = re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x)
        return s[0].lower() + s[1:]

    @staticmethod
    def progress_bar():
        """进度条"""
        t = 60
        logger.info("**************带时间的进度条**************")
        start = time.perf_counter()
        for i in range(t + 1):
            finsh = "▓" * i
            need_do = "-" * (t - i)
            progress = (i / t) * 100
            dur = time.perf_counter() - start
            logger.info("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur))
            time.sleep(0.05)



if __name__ == '__main__':
    StrUtil.progress_bar()
    # logger.info(StrUtil.to_camel_case('UserLoginCount'))  # UserLoginCount
    # logger.info(StrUtil.to_camel_case('userLoginCount'))  # userLoginCount
    # logger.info(StrUtil.to_camel_case('user_login_count'))  # userLoginCount
    # logger.info()
    # logger.info(StrUtil.to_upper_camel_case('UserLoginCount'))  # UserLoginCount
    # logger.info(StrUtil.to_upper_camel_case('userLoginCount'))  # UserLoginCount
    # logger.info(StrUtil.to_upper_camel_case('user_login_count'))  # UserLoginCount
    # logger.info()
    # logger.info(StrUtil.to_lower_camel_case('UserLoginCount'))  # userLoginCount
    # logger.info(StrUtil.to_lower_camel_case('userLoginCount'))  # userLoginCount
    # logger.info(StrUtil.to_lower_camel_case('user_login_count'))  # userLoginCount
    #
    # logger.info()
    #
    # short_name = StrUtil.sub_str_after('t_user_login_count', 't_', True)
    # logger.info(short_name)
    # logger.info(StrUtil.to_upper_camel_case(short_name))  # userLoginCount
    # logger.info(StrUtil.to_lower_camel_case(short_name))  # userLoginCount
    #
    # logger.info(StrUtil.sub_str_after("/Users/shenpeng/Softs/workspaces-py/xinhou-openai-framework", "/", True))
    #
    # db_url = "mysql+pymysql://139.196.122.29:33306/fastapi_admin_db?charset=utf8mb4"
    # db_url_list = db_url.split("//")
    # logger.info("{0}//{1}:{2}@{3}".format(db_url_list[0], "root", "123456", db_url_list[1]))
