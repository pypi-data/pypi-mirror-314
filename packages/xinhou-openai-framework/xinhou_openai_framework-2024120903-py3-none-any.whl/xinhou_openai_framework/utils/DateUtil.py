# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   DateUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/17 17:16   shenpeng   1.0         None
"""

import datetime

from loguru import logger


class DateUtil:
    """
    DateUtil是一个日期处理工具类，提供了常见的日期操作方法。
    """

    @staticmethod
    def get_current_date():
        """
        获取当前日期
        :return: 当前日期，格式为yyyy-mm-dd
        """
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_current_time():
        """
        获取当前时间
        :return: 当前时间，格式为hh:mm:ss
        """
        return datetime.datetime.now().strftime('%H:%M:%S')

    @staticmethod
    def get_current_datetime():
        """
        获取当前日期时间
        :return: 当前日期时间，格式为yyyy-mm-dd hh:mm:ss
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def convert_str_to_date(date_str):
        """
        将字符串日期转换为日期格式
        :param date_str: 字符串日期，格式为yyyy-mm-dd
        :return: 日期格式
        """
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    @staticmethod
    def convert_date_to_str(date):
        """
        将日期格式转换为字符串日期
        :param date: 日期格式
        :return: 字符串日期，格式为yyyy-mm-dd
        """
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def add_days_to_date(date, days):
        """
        在给定日期上添加指定天数
        :param date: 日期格式
        :param days: 要添加的天数
        :return: 新的日期格式
        """
        new_date = date + datetime.timedelta(days=days)
        return new_date

    @staticmethod
    def subtract_days_from_date(date, days):
        """
        在给定日期上减去指定天数
        :param date: 日期格式
        :param days: 要减去的天数
        :return: 新的日期格式
        """
        new_date = date - datetime.timedelta(days=days)
        return new_date

    @staticmethod
    def format_date(date, format_str='%Y-%m-%d'):
        """
        格式化日期
        :param date: 日期格式
        :param format_str: 日期格式字符串，默认为'%Y-%m-%d'
        :return: 格式化后的日期字符串
        """
        return date.strftime(format_str)

    @staticmethod
    def get_first_day_of_month(date):
        """
        获取给定日期所在月份的第一天
        :param date: 日期格式
        :return: 该月的第一天日期格式
        """
        first_day = date.replace(day=1)
        return first_day

    @staticmethod
    def get_last_day_of_month(date):
        """
        获取给定日期所在月份的最后一天
        :param date: 日期格式
        :return: 该月的最后一天日期格式
        """
        next_month = date.replace(day=28) + datetime.timedelta(days=4)
        last_day = next_month - datetime.timedelta(days=next_month.day)
        return last_day

    @staticmethod
    def get_current_timestamp():
        """
        获取当前时间戳（秒级）
        :return: 当前时间戳
        """
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def timestamp_to_datetime(timestamp):
        """
        将时间戳转换为日期时间格式
        :param timestamp: 时间戳
        :return: 日期时间格式
        """
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def datetime_to_timestamp(dt):
        """
        将日期时间格式转换为时间戳
        :param dt: 日期时间格式
        :return: 时间戳
        """
        return int(dt.timestamp())

    @staticmethod
    def format_timestamp(timestamp, format_str='%Y-%m-%d %H:%M:%S'):
        """
        格式化时间戳
        :param timestamp: 时间戳
        :param format_str: 日期时间格式字符串，默认为'%Y-%m-%d %H:%M:%S'
        :return: 格式化后的日期时间字符串
        """
        return DateUtil.timestamp_to_datetime(timestamp).strftime(format_str)


if __name__ == '__main__':
    logger.info('当前日期：', DateUtil.get_current_date())
    logger.info('当前时间：', DateUtil.get_current_time())
    logger.info('当前日期时间：', DateUtil.get_current_datetime())

    # 新添加的方法示例
    today = datetime.date.today()
    logger.info('明天日期：', DateUtil.add_days_to_date(today, 1))
    logger.info('三天前日期：', DateUtil.subtract_days_from_date(today, 3))
    logger.info('格式化日期：', DateUtil.format_date(today, '%A, %B %d, %Y'))
    logger.info('本月第一天：', DateUtil.get_first_day_of_month(today))
    logger.info('本月最后一天：', DateUtil.get_last_day_of_month(today))

    # 时间戳相关方法示例
    current_timestamp = DateUtil.get_current_timestamp()
    logger.info('当前时间戳：', current_timestamp)

    # 将时间戳转换为日期时间格式
    current_datetime = DateUtil.timestamp_to_datetime(current_timestamp)
    logger.info('时间戳转日期时间：', current_datetime)

    # 将日期时间格式转换为时间戳
    another_timestamp = DateUtil.datetime_to_timestamp(current_datetime)
    logger.info('日期时间转时间戳：', another_timestamp)

    # 格式化时间戳
    formatted_timestamp = DateUtil.format_timestamp(current_timestamp, '%Y-%m-%d %H:%M:%S %A')
    logger.info('格式化时间戳：', formatted_timestamp)