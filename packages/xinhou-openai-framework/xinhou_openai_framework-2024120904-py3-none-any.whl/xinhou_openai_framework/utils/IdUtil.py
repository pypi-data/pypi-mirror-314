# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   IdUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 13:09   shenpeng   1.0         None
"""

import uuid

from loguru import logger


class IdUtil:
    """
    ID生成器工具类，支持UUID、UUID32位(去横杠)、Snowflake三种方式生成唯一ID
    """

    @staticmethod
    def uuid():
        """
        生成UUID，格式示例：'7c907db8-058d-4545-a6e8-23b846724feb'
        :return: UUID字符串
        """
        return str(uuid.uuid1())

    @staticmethod
    def uuid_32():
        """
        生成UUID32位，格式示例：'9ad93219dfb04970b57ee8d7b0f2d60c'
        :return: UUID32位字符串
        """
        return str(uuid.uuid1()).replace('-', '')


if __name__ == '__main__':
    # 生成UUID
    logger.info(IdUtil.uuid())
    # 生成UUID32位
    logger.info(IdUtil.uuid_32())
