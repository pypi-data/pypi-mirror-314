# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   PhoneUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 12:50   shenpeng   1.0         None
"""
import re

from loguru import logger


class PhoneUtil:
    """
    PhoneUtil 类：用于判断手机和固定电话。
    支持大陆、香港、台湾、澳门的手机号。
    """

    @staticmethod
    def is_mobile_phone(phone: str) -> bool:
        """
        判断手机号是否合法。
        :param phone: 待判断的手机号。
        :return: True/False，如果是/否合法的手机号。
        """
        # 正则表达式判断手机号是否合法
        pattern = re.compile(r"^1[3-9]\d{9}$")
        return True if pattern.match(phone) else False

    @staticmethod
    def is_fixed_line_phone(phone: str) -> bool:
        """
        判断固定电话是否合法。
        :param phone: 待判断的固定电话。
        :return: True/False，如果是/否合法的固定电话。
        """
        # 正则表达式判断固定电话是否合法
        pattern = re.compile(r"^0\d{2,3}-\d{7,8}$")
        return True if pattern.match(phone) else False


if __name__ == "__main__":
    phone1 = "13800138000"
    logger.info(f"{phone1} 是否是合法的手机号：{PhoneUtil.is_mobile_phone(phone1)}")

    phone2 = "010-12345678"
    logger.info(f"{phone2} 是否是合法的固定电话：{PhoneUtil.is_fixed_line_phone(phone2)}")

