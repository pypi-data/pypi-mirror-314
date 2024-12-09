import logging
import os
from datetime import datetime
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from loguru import logger as loguru_logger


class LoggerManager:

    @staticmethod
    def init_logger(app, log_path: str = None):
        """
        初始化 logger，将日志同时输出到 console 和指定的文件中。
        """
        loguru_logger.remove()
        loguru_logger.add(
            sink=StreamHandler(),
            format="<green>{time:YYYY-MM-DD HH:mm:sss}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> | <level>{message}</level>",
            colorize=True,
            enqueue=True,
        )
        file_info = log_path + f"/{datetime.now().strftime('%Y-%m-%d')}.log"
        os.makedirs(log_path, exist_ok=True)
        if log_path is not None:
            # 创建日志目录
            loguru_logger.add(
                sink=file_info,
                format="{time:YYYY-MM-DD HH:mm:sss} | {level} | {name}:{function}:{line} | {message}",
                rotation="1 day",
                retention="7 days",
                encoding="utf-8",
                compression="zip",
                colorize=True,
                serialize=False,
            )

        # 初始化sqlalchemy日志
        LoggerManager.init_custom_logger('sqlalchemy', file_info)
        # 初始化nacos日志
        LoggerManager.init_custom_logger('nacos', file_info)
        # 初始化skywalking日志
        LoggerManager.init_custom_logger('skywalking', file_info)

    @staticmethod
    def init_custom_logger(name, file_info):
        custom_logger = logging.getLogger(name)
        if not custom_logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            custom_rf_handler = RotatingFileHandler(file_info, maxBytes=1000 * 1024 * 10, backupCount=10)
            custom_rf_handler.setLevel(logging.DEBUG)
            custom_rf_handler.setFormatter(formatter)
            custom_logger.addHandler(custom_rf_handler)
