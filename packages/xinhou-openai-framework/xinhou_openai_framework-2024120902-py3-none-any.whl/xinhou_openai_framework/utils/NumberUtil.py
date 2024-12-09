# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   NumberUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 12:32   shenpeng   1.0         None
"""

from decimal import Decimal, getcontext

from loguru import logger


class NumberUtil:
    """
    数字工具类，提供精确的浮点数运算
    """

    def __init__(self, precision=28):
        """
        初始化
        :param precision: 设置精度，默认为28位
        """
        self.__precision = precision
        getcontext().prec = self.__precision

    def add(self, *args):
        """
        精确加法运算
        :param args: 要相加的数字，可以是多个数字
        :return: 相加结果
        """
        return sum(Decimal(x) for x in args)

    def subtract(self, *args):
        """
        精确减法运算
        :param args: 被减数，减数，可以是多个数字
        :return: 相减结果
        """
        return args[0] - sum(Decimal(x) for x in args[1:])

    def multiply(self, *args):
        """
        精确乘法运算
        :param args: 要相乘的数字，可以是多个数字
        :return: 相乘结果
        """
        result = Decimal(1)
        for x in args:
            result *= Decimal(x)
        return result

    def divide(self, dividend, divisor, decimal_places=None):
        """
        精确除法运算
        :param dividend: 被除数
        :param divisor: 除数
        :param decimal_places: 保留小数位数，默认为None，即保留所有位数
        :return: 相除结果
        """
        result = Decimal(dividend) / Decimal(divisor)
        if decimal_places is None:
            return result
        else:
            return result.quantize(Decimal(f'0.{"0" * decimal_places}'))


if __name__ == '__main__':
    num_util = NumberUtil(5)
    # 加法
    logger.info(num_util.add(1.2903, 2.59, 3.8462))
    # 减法
    logger.info(num_util.subtract(1, 2, 3))
    # 乘法
    logger.info(num_util.multiply(1, 2, 3))
    # 除法


